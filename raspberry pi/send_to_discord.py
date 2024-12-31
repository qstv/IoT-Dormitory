import requests
WEBHOOK_URL ="your_discord_WEBHOOK_URL_here"

def send_message(webhook_url, content, username="倒楣鬼", avatar_url="", embed=None, image_url=None):
    """
    Sends a message to a Discord channel using a webhook, with optional image.

    Args:
        webhook_url (str): The Discord Webhook URL.
        content (str): The text content to send (can be empty if embed is provided).
        username (str, optional): The name to display as the sender. Defaults to None.
        avatar_url (str, optional): The avatar URL for the sender. Defaults to None.
        embed (dict, optional): A dictionary representing embed content. Defaults to None.
        image_url (str, optional): The URL of an image to attach to the message. Defaults to None.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    data = {
        "content": content,
        "username": username,
        "avatar_url": avatar_url,
    }

    if embed:
        data["embeds"] = [embed]

    # Add image if provided (via embed)
    if image_url:
        embed = embed or {}  # Create a new embed if none exists
        embed["image"] = {"url": image_url}
        data["embeds"] = [embed]

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:  # 204 No Content means success
        print("Message sent successfully!")
        return True
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":

    send_message(WEBHOOK_URL, "", embed={
        "title": "警報模式",
        "description": "倒楣鬼拍了一張照片",
        "color": 16711680  # 顏色 (紅色)
    }, image_url="https://picsum.photos/200/300")
