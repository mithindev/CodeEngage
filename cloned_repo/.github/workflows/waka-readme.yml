name: Waka Readme

on:
  workflow_dispatch:
  schedule:
    # Runs at 12am UTC
    - cron: "0 0 * * *"

jobs:
  update-readme:
    name: WakaReadme DevMetrics
    runs-on: ubuntu-latest
    steps:
      - uses: athul/waka-readme@master
        with:
          WAKATIME_API_KEY: ${{ secrets.WAKATIME_API_KEY }}
          SHOW_TITLE: "True"
          SHOW_TOTAL_CODE_TIME: "True"
          SHOW_COMMIT: "True"
          SHOW_DAYS_OF_WEEK: "True"
          SHOW_LANGUAGE: "True"
          SHOW_OS: "True"
          SHOW_PROJECTS: "True"
          SHOW_EDITORS: "True"
          SHOW_LANGUAGE_PER_REPO: "True"
          SHOW_SHORT_INFO: "True"
          
          BLOCKS: ->
          TIME_RANGE: all_time
          SHOW_TIME: true
          SHOW_MASKED_TIME: true
          LANG_COUNT: 10
