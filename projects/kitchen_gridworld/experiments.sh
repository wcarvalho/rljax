make train_search group=uvfa3 search=r2d1

make train_search group=usfa_lstm1 search=usfa_lstm


make train_search group=tasks1 search=r2d1
make train_search group=tasks1 search=usfa_lstm

make train_search group=msf_tasks1 search=msf
make train_search group=msf_modules2 search=msf_modules cuda=0,1,2,3


make train_search group=monolithic2 search=monolithic cuda=0,1,2,3

make train_search group=moredists2 search=moredists cuda=0,1,2,3

make train_search group=lesslang2 search=lesslang cuda=0,1,2,3

make train_search group=bigroom_moredists2 search=bigroom_moredists cuda=0,1,2,3



make train_search group=increasingL2 search=increasingL cuda=0,1,2,3
