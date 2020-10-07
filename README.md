# Capstone Project : ESADE Business School에서 비즈니스 분석 석사 과정용

*AWSKRUG에서 활용을 위해 ReInvent2019의 기본 데이터로 바꾸었습니다.
원문은 아래 깃헙과 블로그를 참고하세요. 구글 번역기로 대충 번역 해 두었습니다.
`dummy-model-for-import/model/model_metadata.json`의 `action_space`를 계산된 값으로 바꾸고 S3로 업로드 후 import_model하고 다시 clone 해서 사용하세요.
`reward_function`과 `hyperparameter`는 model을 clone할 때 변경 가능합니다.*

[원본 깃헙](https://github.com/dgnzlz/Capstone_AWS_DeepRacer) , [설명 블로그](https://towardsdatascience.com/an-advanced-guide-to-aws-deepracer-2b462c37eea)

----
**이 리포지토리에는 "A Advanced Guide to AWS DeepRacer-Autonomous Formula 1 Racing using Reinforcement Learning"기사에 사용 된 코드가 포함되어 있습니다. 먼저 [여기를 클릭](https://towardsdatascience.com/an-advanced-guide-to-aws-deepracer-2b462c37eea)해서 블로그의 내용을 읽어 보시길 바랍니다.**


- `Compute_Speed_And_Actions` 폴더 :  [이곳](https://github.com/cdthompson/deepracer-k1999-race-lines) 저장소에서 최적의 레이싱 라인을 가져와 최적의 속도를 계산하는 jupyter 노트북이 포함되어 있습니다. 
또한 K-Means 클러스터링을 사용하여 사용자 지정 작업 공간을 계산합니다. 이 폴더에는 cdthompson의 K1999 레이싱 라인 노트북도 들어 있는데, 트랙의 내부 `80 %` 만 사용할 수 있도록 변경했습니다.
- `Reward_Function` 폴더 : ~~우리 팀이 2020 년 5 월 F1 이벤트의 타임 트라이얼 부문 참가자 1291 명 중 12 위를 차지하는 데 사용한 보상 기능이 포함 된 .py 파일이 있습니다.~~
  ==> *활용 예시를 위해 **ReInvent2019의 기본 데이터로 바꾸었습니다**. 최적화된 데이터가 아닌 기본 데이터 입니다. 기존 데이터는 [여기 원본 깃헙](https://github.com/dgnzlz/Capstone_AWS_DeepRacer)을 확인해 주세요.*
- `Selenium_Automation` 폴더 : jupyter 노트북이 포함되어있어 AWS CLI를 사용하지 않고 모델을 경주에 여러 번 제출할 수 있습니다. 보너스로 하이퍼 파라미터로 실험을 자동으로 수행 할 수도 있습니다. 몇 시간마다 수동으로 설정할 필요없이 밤새 여러 실험을 수행하는 데 사용할 수 있습니다.

## 사용 된 GitHub 저장소
- 최적의 레이싱 라인 계산 : https://github.com/cdthompson/deepracer-k1999-race-lines
- 로그 분석 : https://github.com/aws-deepracer-community/deepracer-analysis
- 트랙 데이터 검색 : https://github.com/aws-deepracer-community/deepracer-simapp/tree/master/bundle/deepracer_simulation_environment/share/deepracer_simulation_environment/routes

## 라이선스
원하는대로 코드를 자유롭게 사용, 배포 및 변경할 수 있습니다.

이것은 완성 된 대학 프로젝트입니다. 따라서 우리는 더 이상 코드를 유지하지 않을 것입니다.