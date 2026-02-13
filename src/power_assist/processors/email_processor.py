"""Email document processor"""
import os
from typing import Dict, Any
from email import message_from_file
from ..models.document import DocumentContent, DocumentType
from .base import BaseProcessor


class EmailProcessor(BaseProcessor):
    """Processor for Email documents"""
    
    @property
    def supported_type(self) -> DocumentType:
        return DocumentType.EMAIL
    
    async def validate(self, file_path: str) -> bool:
        """Validate Email file"""
        if not os.path.exists(file_path):
            return False
        return file_path.lower().endswith(('.eml', '.msg'))
    
    async def process(self, file_path: str) -> DocumentContent:
        """
        Process Email document
        
        Args:
            file_path: Path to Email file
            
        Returns:
            DocumentContent with extracted information
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                msg = message_from_file(f)
            
            # Extract email components
            subject = msg.get('Subject', 'No Subject')
            from_addr = msg.get('From', 'Unknown')
            to_addr = msg.get('To', 'Unknown')
            date = msg.get('Date', 'Unknown')
            
            # Extract body
            body_parts = []
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body_parts.append(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
            else:
                body_parts.append(msg.get_payload(decode=True).decode('utf-8', errors='ignore'))
            
            body = "\n\n".join(body_parts)
            
            # Format as readable text
            text_content = f"""Subject: {subject}
From: {from_addr}
To: {to_addr}
Date: {date}

{body}
"""
            
            metadata: Dict[str, Any] = {
                "subject": subject,
                "from": from_addr,
                "to": to_addr,
                "date": date,
                "source": file_path,
                "processor": "email",
            }
            
            return DocumentContent(
                text=text_content,
                metadata=metadata,
            )
            
        except Exception as e:
            raise Exception(f"Email processing failed: {str(e)}")
