from typing import Any, Optional
from django.core.management.base import BaseCommand

import apps.telegram.views


class Command(BaseCommand):
    help = "Start Bot Aiogram"

    def handle(self, *args: Any, **options: Any) -> str | None:
        print("START BOT")
        apps.telegram.views.executor.start_polling(apps.telegram.views.dp, skip_updates=True)