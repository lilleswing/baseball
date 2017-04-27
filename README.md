baseball
========
Store a database and analysis of baseball.

## Creating Your Own Database
The data is updated nightly
``` bash
bash devtools/restore_db.sh
sqlite3 baseball.db
.tables
sqlite> .tables
>>  batter       event        game_result  team
>>  calculator   game         pitcher
```

## Looking through my analysis
All my analysis is in ipython [notebooks](/notebooks).

