from .schemas import Post


class MessageFormatter:
    @staticmethod
    def format_post(post: Post) -> str:
        formatted_date = post.created_at.strftime("%Y-%m-%d %H:%M:%S")

        return (
            f"📝 *Заголовок: {post.title}*\n\n"
            f"Текст: {post.text}\n\n"
            f"📅 Время создания: {formatted_date}"
        )
