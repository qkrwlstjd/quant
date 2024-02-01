from scripts.cron.finalized_price_cron_job import PriceFinalizationCronJob
from scripts.cron.unfinalized_price_cron_job import PriceUnfinalizationCronJob

def test_cron_job_execution():
    # 크론 작업 클래스의 인스턴스 생성
    cron_job = PriceFinalizationCronJob()
    cron_job2 = PriceUnfinalizationCronJob()
    # 크론 작업을 실행
    cron_job.do()
    cron_job2.do()

    # 작업 실행 결과를 확인하고 검증
    # 예를 들어, 데이터베이스에 예상된 레코드가 추가되었는지 확인 가능