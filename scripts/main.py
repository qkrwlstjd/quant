import os
import sys
import time



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantProject.settings')  # 'your_project'는 실제 프로젝트 이름으로 변경해야 합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import django

if __name__ == "__main__":
    while True:
        try:
            django.setup()
            from scripts.script import main_script
            start_time = time.time()
            main_script()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Function execution time: {execution_time} seconds")
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            time.sleep(5)  # 재시도 전에 1초 대기


