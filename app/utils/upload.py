import os
import uuid
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import magic

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    errors = []
    
    if not file:
        errors.append("No file provided")
        return errors
        
    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        errors.append(f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB")
        
    # Check file extension
    if not allowed_file(file.filename):
        errors.append("File type not allowed. Allowed types: " + ", ".join(ALLOWED_EXTENSIONS))
        
    # Verify file content type
    file_content = file.read(2048)
    file.seek(0)
    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(file_content)
    
    if not content_type.startswith('image/'):
        errors.append("File must be an image")
        
    return errors

def optimize_image(file):
    """Optimize image for storage"""
    try:
        image = Image.open(file)
        
        # Convert to RGB if necessary
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')
            
        # Resize if too large while maintaining aspect ratio
        max_size = (800, 800)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
        # Save optimized image
        output = BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

class S3Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket = os.getenv('AWS_S3_BUCKET')
        
    def upload_file(self, file, folder='profile-images'):
        try:
            # Generate unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{folder}/{str(uuid.uuid4())}.{ext}"
            
            # Optimize image
            optimized_file = optimize_image(file)
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                optimized_file,
                self.bucket,
                filename,
                ExtraArgs={
                    'ContentType': 'image/jpeg',
                    'ACL': 'public-read'
                }
            )
            
            # Return public URL
            return f"https://{self.bucket}.s3.amazonaws.com/{filename}"
            
        except ClientError as e:
            raise ValueError(f"Error uploading to S3: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing upload: {str(e)}")

class LocalUploader:
    def __init__(self):
        self.upload_folder = os.path.join(os.getcwd(), 'uploads', 'profile-images')
        os.makedirs(self.upload_folder, exist_ok=True)
        
    def upload_file(self, file):
        try:
            # Generate unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{str(uuid.uuid4())}.{ext}"
            filepath = os.path.join(self.upload_folder, filename)
            
            # Optimize image
            optimized_file = optimize_image(file)
            
            # Save to local storage
            with open(filepath, 'wb') as f:
                f.write(optimized_file.getvalue())
            
            # Return local URL
            return f"/uploads/profile-images/{filename}"
            
        except Exception as e:
            raise ValueError(f"Error processing upload: {str(e)}")

# Choose uploader based on configuration
def get_uploader():
    if os.getenv('USE_S3', 'false').lower() == 'true':
        return S3Uploader()
    return LocalUploader() 