from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Blog


fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--num",
            type=int,
            default=10,
        )

    def handle(self, *args, **options):
        Blog.objects.all().delete()

        num = options["num"]

        for _ in range(num):
            fake_title = fake.sentence()
            fake_content = fake.text(max_nb_chars=1500)
            Blog.objects.create(title=fake_title, content=fake_content)

        self.stdout.write(self.style.SUCCESS(f"Succesfully generated {num} blogs"))
