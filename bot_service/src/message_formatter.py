from .schemas import Post


class MessageFormatter:
    @staticmethod
    def format_post(post: Post) -> str:
        formatted_date = post.created_at.strftime("%Y-%m-%d %H:%M:%S")

        return f"📝 *{post.title}*\n\n" f"{post.text}\n\n" f"📅 Created: {formatted_date}"
