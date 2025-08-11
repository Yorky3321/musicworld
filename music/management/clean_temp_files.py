import os
import time
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "刪除 media/temp 資料夾中過舊的暫存檔案"

    def handle(self, *args, **options):
        temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
        expiration_seconds = 60 * 30  # 刪除超過 30 分鐘未使用的檔案

        if not os.path.exists(temp_dir):
            self.stdout.write(self.style.WARNING(f"找不到資料夾：{temp_dir}"))
            return

        now = time.time()
        deleted_count = 0

        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)

            # 只清除 .wav 和 .mid 檔
            if not filename.endswith((".wav", ".mid")):
                continue

            try:
                modified_time = os.path.getmtime(filepath)
                if now - modified_time > expiration_seconds:
                    os.remove(filepath)
                    deleted_count += 1
                    self.stdout.write(f"刪除檔案：{filename}")
            except Exception as e:
                self.stderr.write(f"錯誤處理 {filename}：{e}")

        self.stdout.write(self.style.SUCCESS(f"共刪除 {deleted_count} 個過期檔案"))
