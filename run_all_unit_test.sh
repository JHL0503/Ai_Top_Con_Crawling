################################################
# 설정 부분
################################################
# 이 변수에는 절대경로를 넣으셔야 합니다.
# 이 변수를 설정하면 모든 unit test의 로그가 .log 파일 하나에 기록됩니다.
# 이 변수를 설정하지 않으면, 모든 unit test의 로그는 각 unit test가 위치하는
# dir 속 log dir에 각각 기록됩니다.
export LOG_LOCATION=""
#export LOG_LOCATION="/home/jjtopology/GenerativeAI/Ai_Top_Con_Crawling/ut_log"

export LOG_LEVEL="DEBUG"


# 이걸 안해주면 'from src' 부분을 못잡더라.
export PYTHONPATH="$PWD:$PYTHONPATH"


################################################
# 실행 부분 (Don't touch)
################################################
# 먼저 unit test들이 모여있는 dir로 이동합니다.
cd ./tests

# 다음으로 ./tests 속에 있는 'Test'로 시작하는 하위 dir 속으로 이동 한 다음
# unittest 모듈을 이용해서 하위 unit test들을 모두 실행하고 나옵니다.
# 주의점이 'Test'로 시작해야 한다는 것입니다.
for item in ./Test*; do
  # 디렉토리인지 확인
  if [ -d "$item" ]; then
    cd $item
    echo "Run the unit test codes in dir: $(basename "$item")"
    python -m unittest discover
    cd ..
  fi
done
