# myapp/management/commands/mycommand.py

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Describe what this command does'

    def add_arguments(self, parser):
        # 명령어 인자 추가 (선택적)
        parser.add_argument('sample_arg', type=int)

    def handle(self, *args, **options):
        sample_arg = options['sample_arg']
        # 실제 명령어 로직 구현
        self.stdout.write(self.style.SUCCESS('Successfully executed command'))
