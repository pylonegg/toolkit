import win32com.client
from datetime import datetime

# Initialize Outlook application
outlook_app = win32com.client.Dispatch("Outlook.Application")
namespace = outlook_app.GetNamespace("MAPI")  # Correct namespace object
inbox = namespace.GetDefaultFolder(6)  # 6 = Inbox folder


def read_inbox(max_emails=20):
    """Fetch recent emails from Outlook inbox (folder 'test') and return as dicts."""
    try:
        folder = inbox.Folders.Item("test")  # Replace 'test' with your folder name
        messages = folder.Items
        messages.Sort("[ReceivedTime]", True)  # Sort descending
    except Exception as e:
        print(f"[ERROR] Cannot access folder: {e}")
        return []

    tasks = []
    for i, msg in enumerate(messages):
        if i >= max_emails:
            break
        try:
            tasks.append({
                "object_ref": msg.EntryID,
                "sender": msg.SenderEmailAddress,
                "subject": msg.Subject,
                "body": msg.Body,
                "received": msg.ReceivedTime,
                "source": "Outlook"
            })
        except Exception as e:
            print(f"[WARNING] Error reading email {i}: {e}")
            continue

    print(f"[INFO] Retrieved {len(tasks)} emails from folder '{folder.Name}'.")
    return tasks


def create_draft_email(message_id, body):
    """
    Create a draft reply to a specific email by EntryID.
    Preserves conversation thread and ensures proper line breaks.
    """
    try:
        msg = namespace.GetItemFromID(message_id)
        if not msg:
            print(f"[WARNING] Message ID {message_id} not found.")
            return None

        reply = msg.Reply()

        if hasattr(msg, "HTMLBody") and msg.HTMLBody:
            # Ensure AI body has paragraphs and add blockquote for original email
            body_html = body.replace("\n", "<br>")  # Convert newlines to <br>
            reply.HTMLBody = f"<p>{body_html}</p><br>{msg.HTMLBody}"
        else:
            # For plain text, use CRLF line breaks
            reply.Body = f"{body}\r\n\r\n--- Original Message ---\r\n{msg.Body}"

        reply.Save()
        print(f"[INFO] Draft created successfully for Message ID {message_id}.")
        return reply.EntryID

    except Exception as e:
        print(f"[ERROR] Failed to create draft for Message ID {message_id}: {e}")
        return None
