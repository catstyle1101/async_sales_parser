# sales_parser
Async version sales parser for making sales rating for daily control (twice + faster!)
Uses tqdm for progress bar when async scrapping

## Using
Run main.py

## Result

```
❗❗❗❗❗❗❗❗❗❗
Результаты продаж менеджеров:
🏆 Иванова Н.В.  ГО: 11 304 119  медиана:  153 545 ПКБ: 25
🥈 Петрова А.А. ГО: 10 999 466  медиана:  141 089 ПКБ: 14
🥉 Сидорова Д.В. ГО:  7 974 506  медиана:   92 241 ПКБ: 12
Козлова Е.А.     ГО:  6 698 586  медиана:   91 904 ПКБ: 22
Симонова С.В.    ГО:  5 961 072  медиана:   29 181 ПКБ: 12
❗❗❗❗❗❗❗❗❗❗
```
A string for paste to Skype/telegram message
Ordered ascending by sum of sales
first three manager are highlighted by emoji
