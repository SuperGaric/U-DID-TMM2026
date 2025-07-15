保留问题：
[1] 最终数据处理问题：数据整理问题，我在/home/dmt/multiple_UEs/experimentdata/withDID/large_experiment下建了nue_withDID_n的文件夹，每个都是一个nue_withDID的测试数据，到时候要先平均，再grep再画图，但是我想到了一个方法，是先grep，这样每个文件夹都会出一个图的数据，然后再对grep好的进行平均，这样要轻松很多。

[2] UE大规模数据上不去的问题，目前核心网一次性鉴权的数量有限，我反复启动可以提高，报错是这样的：（如下记录）

（而且还有一个问题，每次amf受到的ue鉴权都不全，总会留部分没有鉴权全。）
[NR_MAC]   [RAPROC][974.17] RA-Msg3 transmitted
[NR_MAC]   Adding new UE context with RNTI 0x9d0f
[NR_MAC]   Try to add UE 9d0f but the list is full
[NR_MAC]   Remove NR rnti 0x9d0f
[NR_MAC]   Random Access 0 discarded at state WAIT_Msg3 (TC_RNTI 9d0f RNTI 9d0f): max number of users achieved!
[NR_MAC]   no RA proc for RNTI 0x9d0f in Msg3/PUSCH
[NR_MAC]   PRACH scheduler: Selected RO Frame 975, Slot 19, Symbol 0, Fdm 0
[NR_RRC]   Timer T300 expired! No timely response to RRCSetupRequest
[PHY]   PRACH [UE 0] in frame.slot 975.19, placing PRACH in position 2828, msg1 frequency start 0 (k1 0), preamble_offset 1, first_nonzero_root_idx 0
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   RSRP = -42 dBm
[NR_PHY]   [RAPROC] 975.19 Initiating RA procedure with preamble 6, energy 54.0 dB (I0 148, thres 120), delay 0 start symbol 0 freq index 0
[NR_MAC]   975.19 UE RA-RNTI 010b TC-RNTI ab93: Activating RA process index 0
[NR_MAC]   NR band duplex spacing is 0 KHz (nr_bandtable[40].band = 78)
[NR_MAC]   NR band 78, duplex mode TDD, duplex spacing = 0 KHz
[NR_MAC]   Initialization of 4-step contention-based random access procedure
[NR_MAC]   UE ab93: 976.7 Generating RA-Msg2 DCI, RA RNTI 0x10b, state 1, CoreSetType 0, RAPID 6
[NR_MAC]   UE ab93: Msg3 scheduled at 976.17 (976.7 k2 7 TDA 3)
[NR_MAC]   Starting RA Contention Resolution timer with 64 ms + 2 * 7 K2 (142 slots) duration
[MAC]   [UE 0][976:9] RAR reception failed 
[MAC]   [UE 0][976:9] RAR reception failed 
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (9)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (42)
[MAC]   [UE 0][976:9] RAR reception failed 
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (16)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (57)
[PHY]   RAR-Msg2 decoded
[MAC]   [UE 0][976:9] RAR reception failed 
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (18)
[PHY]   RAR-Msg2 decoded
[MAC]   [UE 0][976:9] RAR reception failed 
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267rfsimulator_write_internal(t, t->lastWroteTS > 1 ? t->lastWroteTS - 1 : 0, samplesVoid, 1, t->tx_num_channels, 1, false);
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (42)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (9)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (5)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (56)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][976.7] Received RAR preamble (6) doesn't match the intended RAPID (53)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[PHY]   RAR-Msg2 decoded
65535208950000000033|               |               1|         57| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      3|     5GMM-DEREGISTERED|   208950000000036|               |              13|         52| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      4|     5GMM-DEREGISTERED|   208950000000039|               |               9|         70| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      5|     5GMM-DEREGISTERED|   208950000000040|               |              11|         73| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      6|     5GMM-DEREGISTERED|   208950000000043|               |               5|         62| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      7|     5GMM-DEREGISTERED|   208950000000044|               |               8|         24| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      8|     5GMM-DEREGISTERED|   208950000000045|               |               7|          4| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |      9|     5GMM-DEREGISTERED|   208950000000046|               |               8|         49| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     10|     5GMM-DEREGISTERED|   208950000000047|               |               3|          1| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     11|     5GMM-DEREGISTERED|   208950000000049|               |              10|         28| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     12|     5GMM-DEREGISTERED|   208950000000050|               |               7|         67| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     13|     5GMM-DEREGISTERED|   208950000000051|               |               2|         59| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     14|     5GMM-DEREGISTERED|   208950000000052|               |              13|         31| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     15|     5GMM-DEREGISTERED|   208950000000053|               |              12|         10| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     16|     5GMM-DEREGISTERED|   208950000000054|               |               8|         69| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     17|     5GMM-DEREGISTERED|   208950000000055|               |              13|         77| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     18|     5GMM-DEREGISTERED|   208950000000056|               |               2|         38| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     19|     5GMM-DEREGISTERED|   208950000000057|               |               6|         66| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     20|     5GMM-DEREGISTERED|   208950000000058|               |               4|         19| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     21|     5GMM-DEREGISTERED|   208950000000059|               |              11|         50| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     22|     5GMM-DEREGISTERED|   208950000000061|               |              14|         33| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     23|     5GMM-DEREGISTERED|   208950000000062|               |              16|         56| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     24|     5GMM-DEREGISTERED|   208950000000063|               |              10|         48| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     25|     5GMM-DEREGISTERED|   208950000000064|               |               7|         23| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     26|     5GMM-DEREGISTERED|   208950000000066|               |              14|         79| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     27|     5GMM-DEREGISTERED|   208950000000067|               |               6|         22| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     28|     5GMM-DEREGISTERED|   208950000000068|               |               8|          7| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     29|     5GMM-DEREGISTERED|   208950000000070|               |              15|         80| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     30|     5GMM-DEREGISTERED|   208950000000071|               |              14|         54| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     31|     5GMM-DEREGISTERED|   208950000000072|               |               3|         64| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     31|     5GMM-DEREGISTERED|   208950000000072|               |               3|         64| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     32|     5GMM-DEREGISTERED|   208950000000073|               |               3|         40| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.785] [amf_app] [info] |     33|     5GMM-DEREGISTERED|   65535
[2024-12-12 16:27:54.786] [amf_app] [info] |     38|     5GMM-DEREGISTERED|   208950000000079|               |               1|         37| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     39|     5GMM-DEREGISTERED|   208950000000080|               |               3|         17| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     40|     5GMM-DEREGISTERED|   208950000000083|               |               6|         44| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     41|     5GMM-DEREGISTERED|   208950000000084|               |              13|         11| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     42|     5GMM-DEREGISTERED|   208950000000085|               |               4|         60| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     43|     5GMM-DEREGISTERED|   208950000000086|               |              16|         36| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |     44|     5GMM-DEREGISTERED|   208950000000087|               |              12|         51| 208, 95 |0x   e00000|
[2024-12-12 16:27:54.786] [amf_app] [info] |--------------------------------------------------------------------------------------------------------------------|

我觉得奥，可能是harq，或者上行链路之类的，空间不够，

#define MAX_MOBILES_PER_ENB 40 但是基本确定了可能和他没什么关系？可以配置了之后试试，因为目前数量超过了40





[MAC]   received TA command 31
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][604.7] Received RAR preamble (19) doesn't match the intended RAPID (28)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   [RAPROC][604.17] RA-Msg3 transmitted
[NR_MAC]   Adding new UE context with RNTI 0x0c7c
[NR_MAC]   Try to add UE 0c7c but the list is full
[NR_MAC]   Remove NR rnti 0x0c7c
[NR_MAC]   Random Access 0 discarded at state WAIT_Msg3 (TC_RNTI 0c7c RNTI 0c7c): max number of users achieved!
[NR_MAC]   no RA proc for RNTI 0x0c7c in Msg3/PUSCH
[NR_MAC]   PRACH scheduler: Selected RO Frame 605, Slot 19, Symbol 0, Fdm 0
[PHY]   PRACH [UE 0] in frame.slot 605.19, placing PRACH in position 2828, msg1 frequency start 0 (k1 0), preamble_offset 11, first_nonzero_root_idx 0
[NR_PHY]   [RAPROC] 605.19 Initiating RA procedure with preamble 46, energy 54.0 dB (I0 125, thres 120), delay 0 start symbol 0 freq index 0
[NR_MAC]   605.19 UE RA-RNTI 010b TC-RNTI 4fa8: Activating RA process index 0
[NR_MAC]   UE 4fa8: 606.7 Generating RA-Msg2 DCI, RA RNTI 0x10b, state 1, CoreSetType 0, RAPID 46
[NR_MAC]   UE 4fa8: Msg3 scheduled at 606.17 (606.7 k2 7 TDA 3)
[NR_MAC]   Starting RA Contention Resolution timer with 64 ms + 2 * 7 K2 (142 slots) duration
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   Trying to process acknack for an inactive harq process (0)


[NR_MAC]   Try to add UE 95fe but the list is full
[NR_MAC]   Remove NR rnti 0x95fe
[NR_MAC]   Random Access 0 discarded at state WAIT_Msg3 (TC_RNTI 95fe RNTI 95fe): max number of users achieved!
[NR_MAC]   no RA proc for RNTI 0x95fe in Msg3/PUSCH
[NR_MAC]   PRACH scheduler: Selected RO Frame 1005, Slot 19, Symbol 0, Fdm 0
[PHY]   PRACH [UE 0] in frame.slot 1005.19, placing PRACH in position 2828, msg1 frequency start 0 (k1 0), preamble_offset 14, first_nonzero_root_idx 0
[NR_RRC]   Timer T300 expired! No timely response to RRCSetupRequest
[NR_PHY]   [RAPROC] 1005.19 Initiating RA procedure with preamble 56, energy 54.0 dB (I0 154, thres 120), delay 0 start symbol 0 freq index 0
[NR_MAC]   1005.19 UE RA-RNTI 010b TC-RNTI 7d52: Activating RA process index 0
[NR_MAC]   NR band duplex spacing is 0 KHz (nr_bandtable[40].band = 78)
[NR_MAC]   NR band 78, duplex mode TDD, duplex spacing = 0 KHz
[NR_MAC]   Initialization of 4-step contention-based random access procedure
[NR_MAC]   UE 7d52: 1006.7 Generating RA-Msg2 DCI, RA RNTI 0x10b, state 1, CoreSetType 0, RAPID 56
[NR_MAC]   UE 7d52: Msg3 scheduled at 1006.17 (1006.7 k2 7 TDA 3)
[NR_MAC]   Starting RA Contention Resolution timer with 64 ms + 2 * 7 K2 (142 slots) duration
[NR_MAC]   Trying to process acknack for an inactive harq process (0)





CCE

harq

gnb莫名down掉了

[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][634.7] Received RAR preamble (21) doesn't match the intended RAPID (20)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][634.7] Received RAR preamble (21) doesn't match the intended RAPID (57)
[PHY]   RAR-Msg2 decoded
Average CPU Usage: 6.54%
Average Memory Usage: 85.98 MB
Average CPU Usage: 6.26%
Average Memory Usage: 85.99 MB
Average CPU Usage: 6.52%
Average Memory Usage: 85.98 MB
Average CPU Usage: 6.17%
Average Memory Usage: 85.98 MB
Average CPU Usage: 6.28%
Average Memory Usage: 85.98 MB
Average CPU Usage: 6.00%
Average Memory Usage: 85.99 MB
[NR_MAC]   [RAPROC][634.17] RA-Msg3 transmitted
Average CPU Usage: 5.91%
Average Memory Usage: 85.99 MB
[NR_MAC]   Random Access 0 failed at state WAIT_Msg3 (TC_RNTI a849 RNTI 4354)
[NR_MAC]   Adding new UE context with RNTI 0x4354
Average CPU Usage: 5.85%
Average Memory Usage: 85.99 MB
[NR_MAC]   [gNB 0][RAPROC] PUSCH with TC_RNTI 0x4354 received correctly, adding UE MAC Context RNTI 0x4354
[NR_MAC]   [RAPROC] RA-Msg3 received (sdu_lenP 7)

Assertion (offset < 320) failed!
In set_csi_meas_periodicity() ../../../openair2/RRC/NR/nr_rrc_config.c:1516
Not enough UL slots to accomodate all possible UEs. Need to rework the implementation

Exiting execution
../../../openair2/RRC/NR/nr_rrc_config.c:1516 set_csi_meas_periodicity() Exiting OAI softmodem: _Assert_Exit_
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Lost socket
[HW]   Received data on not connected socket 103
[HW]   Received data on not connected socket 104
[HW]   Received data on not connected socket 105
[HW]   Received data on not connected socket 106
[HW]   Lost socket
[HW]   Received data on not connected socket 107
[HW]   Received data on not connected socket 108
[HW]   Received data on not connected socket 109
[HW]   Received data on not connected socket 110
[HW]   Received data on not connected socket 113
[HW]   Received data on not connected socket 115
[HW]   Received data on not connected socket 111
[HW]   Received data on not connected socket 112
[HW]   Received data on not connected socket 116
[HW]   Received data on not connected socket 114
[HW]   Received data on not connected socket 117
[HW]   recv() failed, errno(9)
[HW]   Lost socket
[HW]   Lost socket
[HW]   Received data on not connected socket 119
[HW]   recv() failed, errno(9)
[HW]   Lost socket
[HW]   Lost socket

succeed

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --sa --uicc0.imsi 208950000000031 --rfsim



sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600000000 --sa --uicc0.imsi 208950000000033 --rfsim

<!-- 1~2 -->

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600090000 --sa --uicc0.imsi 208950000000033 --rfsim （sync）

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600120000 --sa --uicc0.imsi 208950000000033 --rfsim (sync)

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600150000 --sa --uicc0.imsi 208950000000033 --rfsim (sync)

<!-- sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600180000 --sa --uicc0.imsi 208950000000033 --rfsim (failed) -->

<!-- sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600210000 --sa --uicc0.imsi 208950000000033 --rfsim -->

<!-- sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600240000 --sa --uicc0.imsi 208950000000033 --rfsim -->

<!-- sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600270000 --sa --uicc0.imsi 208950000000033 --rfsim -->

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3600300000 --sa --uicc0.imsi 208950000000033 --rfsim


sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3338160000 --sa --uicc0.imsi 208950000000033 --rfsim （sync）

<!-- sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3638160000 --sa --uicc0.imsi 208950000000033 --rfsim  -->

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3638400000 --sa --uicc0.imsi 208950000000034 --rfsim (succeed)

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3657600000 --sa --uicc0.imsi 208950000000035 --rfsim (succeed)

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --sa --uicc0.imsi 208950000000036 --rfsim (succeed)

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3676800000 --sa --uicc0.imsi 208950000000036 --rfsim (succeed)

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3696000000 --sa --uicc0.imsi 208950000000037 --rfsim (succeed)
65535
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][546.7] Received RAR preamble (19) doesn't match the intended RAPID (47)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   Trying to process acknack for an inactive harq process (0)
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 0005] Got BI RAR subPDU 267 ms
[NR_MAC]   [UE 0][RAPROC][RA-RNTI 010b] Got RAPID RAR subPDU
[NR_MAC]   [UE 0][RAPROC][546.7] Received RAR preamble (19) doesn't match the intended RAPID (55)
[PHY]   RAR-Msg2 decoded
[NR_MAC]   [RAPROC][546.17] RA-Msg3 transmitted
[NR_MAC]   Adding new UE context with RNTI 0x49fb
[NR_MAC]   [gNB 0][RAPROC] PUSCH with TC_RNTI 0x49fb received correctly, adding UE MAC Context RNTI 0x49fb
[NR_MAC]   [RAPROC] RA-Msg3 received (sdu_lenP 7)

Assertion (offset < 320) failed!
In set_csi_meas_periodicity() ../../../openair2/RRC/NR/nr_rrc_config.c:1516
Not enough UL slots to accomodate all possible UEs. Need to rework the implementation

Exiting execution
../../../openair2/RRC/NR/nr_rrc_config.c:1516 set_csi_meas_periodicity() Exiting OAI softmodem: _Assert_Exit_



新错误
[NR_MAC]   Starting RA Contention Resolution timer with 64 ms + 2 * 7 K2 (142 slots) duration
[NR_MAC]   No signal
[NR_MAC]   no RA proc for RNTI 0xc66f in Msg3/PUSCH
[NR_MAC]   UE 9749: reported RSRP index 118 invalid
[NR_MAC]   UE 9749: reported RSRP index 118 invalid


Assertion (enc_rval.encoded > 0 && enc_rval.encoded <= max_buffer_size * 8) failed!
In encode_cellGroupConfig() ../../../openair2/RRC/NR/nr_rrc_config.c:3002
ASN1 message encoding failed (csi-ReportConfigToAddModList, 18446744073709551615)!


目前修改的地方
openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_primitives.c
  // uint8_t du2cu[1024];
  uint8_t du2cu[8192]; //先试试4096可不可以

  我很奇怪，这里变了，为啥还是溢出


openair2/RRC/NR/nr_rrc_config.c
    const int idx = (uid << 1) + is_rsrp;
  const int offset = first_ul_slot_period + idx % n_ul_slots_period + (idx / n_ul_slots_period) * n_slots_period;
  // AssertFatal(offset < 320, "Not enough UL slots to accomodate all possible UEs. Need to rework the implementation\n");
  AssertFatal(offset < 1000, "Not enough UL slots to accomodate all possible UEs. Need to rework the implementation\n");




  Assertion (enc_rval.encoded > 0 && enc_rval.encoded <= max_buffer_size * 8) failed!
In encode_cellGroupConfig() ../../../openair2/RRC/NR/nr_rrc_config.c:3002
ASN1 message encoding failed (csi-ReportConfigToAddModList, 18446744073709551615), max_buffer_size*8: (65536)!

    【我很奇怪，这里变了，为啥还是溢出；】 确实该溢出，
    但是他的意思是这个


【注册不全的问题】
    [2024-12-17 16:21:18.733] [amf_n1] [debug] Signal the UE CommunicationFailure Report Event notification for SUPI imsi-208950000000031
[2024-12-17 16:21:18.733] [amf_n2] [info] Received Downlink NAS Transport message, handling
[2024-12-17 16:21:18.733] [amf_n2] [debug] Handle DL NAS Transport ...
[2024-12-17 16:21:18.733] [amf_n1] [debug] Send request to SBI to trigger UE Communication Failure Report (SUPI imsi-208950000000031 )


 ##  现在就是两条路：1、规模问题，先解决gnb掉线问题，再解决数量问题，这两个可能是一个问题；2、解决注册不全问题。 
 ##  24-12-17 决定先解决规模问题 

 现在的配置是

 /home/ubuntu/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/openairinterface5g_withoutDID/common

 #ifndef OPENAIRINTERFACE5G_LIMITS_H_
#define OPENAIRINTERFACE5G_LIMITS_H_

#        define MAX_MOBILES_PER_GNB 200 //16
#        define NUMBER_OF_eNB_MAX 1
#        define NUMBER_OF_gNB_MAX 1
#        define NUMBER_OF_RU_MAX 2
#        define NUMBER_OF_NR_RU_MAX 2
#        define NUMBER_OF_UCI_MAX 16 //16
#        define NUMBER_OF_ULSCH_MAX 8 //8
#        define NUMBER_OF_DLSCH_MAX 8 //8 
#        define NUMBER_OF_SRS_MAX 16 //16
#        define NUMBER_OF_SCH_STATS_MAX 16 //16

#define MAX_MANAGED_ENB_PER_MOBILE  2
#define MAX_MANAGED_GNB_PER_MOBILE  2

#        ifndef PHYSIM
#            ifndef UE_EXPANSION
#                    define NUMBER_OF_UE_MAX 200 //40
#                    define NUMBER_OF_CONNECTED_eNB_MAX 1
#                    define NUMBER_OF_CONNECTED_gNB_MAX 1
#            else
#                    define NUMBER_OF_UE_MAX 256
#                    define NUMBER_OF_CONNECTED_eNB_MAX 1
#                    define NUMBER_OF_CONNECTED_gNB_MAX 1
#            endif
#        else
#                    define NUMBER_OF_UE_MAX 4
#                    define NUMBER_OF_CONNECTED_eNB_MAX 1
#                    define NUMBER_OF_CONNECTED_gNB_MAX 1
#        endif

#endif /* OPENAIRINTERFACE5G_LIMITS_H_ */


50 UE 全部3.6192GHz 频段，连接顺利，但是之上到核心网44个，且有一半左右没有注册
45 UE ....                                    42个，比一半好一点点



【文件描述符限制（1024）太低：】
ulimit -n 返回 1024
这表示当前用户的 最大文件描述符数量 是 1024。

netstat -an | wc -l 返回 1405
这显示当前系统上已经有 1405 个网络连接或 socket（包括监听、已建立、等待状态等）。

ulimit -n 65535

ulimit -n


2. 永久增加文件描述符限制

步骤 1：修改用户配置文件
编辑 /etc/security/limits.conf，为当前用户增加限制：

sudo nano /etc/security/limits.conf

添加以下两行（将 ubuntu 替换为你的用户名）：

ubuntu hard nofile 65535
ubuntu soft nofile 65535


试试描述符的问题




[24-12-17-23:38  01]
报错解析

报错信息表明在 encode_cellGroupConfig() 函数中，ASN.1 编码失败了。enc_rval.encoded 的值被检测到为 负数或无效值，具体错误出现在对 NR_CellGroupConfig_t 结构的编码过程中：

AssertFatal(enc_rval.encoded > 0 && enc_rval.encoded <= max_buffer_size * 8,
            "ASN1 message encoding failed (%s, %lu)!\n",
            enc_rval.failed_type->name,
            enc_rval.encoded);

    enc_rval.encoded 表示编码后的 位数。
    enc_rval.failed_type->name 给出 失败的结构体类型，这里失败的类型是 csi-ReportConfigToAddModList。

18446744073709551615 表示 uint64_t 类型的最大值，意味着 enc_rval.encoded 发生了溢出，或者编码过程中出错，导致值不正常。
问题排查思路

    检查 cellGroupConfig 的完整性
    编码失败很可能是因为 NR_CellGroupConfig_t 结构中的某个字段配置不正确或未初始化，特别是报错中提到的 csi-ReportConfigToAddModList 字段。
        csi-ReportConfigToAddModList 是用于 CSI（信道状态信息）报告配置的字段。如果这个字段为空，或者其内容不符合 ASN.1 规范，就可能导致编码失败。
        解决方法：HPLMN= "20893";
cellGroupConfig 是通过 get_initial_cellGroupConfig() 函数生成的。你需要深入该函数，逐一检查 NR_CellGroupConfig_t 的各个子字段，确保所有必要的参数都被正确设置。

重点关注：

    rlc_BearerToAddModList
    mac_CellGroupConfig
    physicalCellGroupConfig
    csi-ReportConfigToAddModList

如果某个字段不符合规范，编码器将失败。

查看 ASN.1 编码器的限制

    编码器函数 uper_encode_to_buffer() 使用的 ASN.1 描述符是 asn_DEF_NR_CellGroupConfig。
    如果 cellGroupConfig 内部数据超出了描述符定义的范围，编码会失败。
    检查 csi-ReportConfigToAddModList 是否超出标准范围或包含不支持的配置。

调试输出 cellGroupConfig 内容
在调用 encode_cellGroupConfig() 前，打印 cellGroupConfig 结构体的内容，确认其中的字段是否存在异常值或者未初始化的情况。

示例调试代码：

if (cellGroupConfig->csi_ReportConfigToAddModList != NULL) {
    printf("csi-ReportConfigToAddModList count: %d\n",
           cellGroupConfig->csi_ReportConfigToAddModList->list.count);
} else {
    printf("csi-ReportConfigToAddModList is NULL\n");
}

缓冲区大小检查
buffer 和 max_buffer_size 传入 ASN.1 编码器时，需要足够大以容纳编码后的数据。如果缓冲区太小，会导致编码失败。

    在 prepare_initial_ul_rrc_message() 中，分配的缓冲区大小是 1024 字节，你可以尝试增大这个缓冲区：

uint8_t du2cu[2048];  // 增大缓冲区

启用 ASN.1 编码调试输出
如果编码器提供调试功能，可以启用详细输出，查看具体失败的原因。

    asn_debug = 1;  // 启用 ASN.1 编码器调试信息

    验证 ASN.1 规范版本
    检查项目使用的 ASN.1 规范是否与 3GPP 38.331 标准定义一致。如果存在版本不匹配，也会导致编码器解析失败。

临时解决方案

如果你确定 csi-ReportConfigToAddModList 是不必要的，可以在 get_initial_cellGroupConfig() 中将其置空，然后重新尝试编码。

cellGroupConfig->csi_ReportConfigToAddModList = NULL;





[24-12-17-23:38  02]
根据你提供的报错信息：

Assertion (enc_rval.encoded > 0 && enc_rval.encoded <= max_buffer_size * 8) failed!
ASN1 message encoding failed (csi-ReportConfigToAddModList, 18446744073709551615)

问题集中在 encode_cellGroupConfig() 中的 uper_encode_to_buffer() 调用。enc_rval.encoded 的值是 -1，但被解释为了最大值 18446744073709551615（无符号整数的最大值），表明编码失败。
排查思路
1. 输入数据不完整或不符合规范

    NR_CellGroupConfig_t 结构体可能存在未正确初始化的字段，导致编码失败。
    检查重点：
        rlc_BearerToAddModList
        mac_CellGroupConfig
        physicalCellGroupConfig
        spCellConfig
    确保结构体中 所有必填字段 都已初始化，特别是任何指针或动态分配的列表。

2. rlc_BearerToAddModList 的内容不合法

报错信息中提到了 csi-ReportConfigToAddModList，表明在生成 NR_CellGroupConfig 时可能与某些配置相关联。

    检查 rlc_BearerToAddModList 中的 NR_RLC_BearerConfig 是否有效且正确初始化。
    确保 NR_RLC_BearerConfig 中的 servedRadioBearer、logicalChannelIdentity、mac_LogicalChannelConfig 等字段都被正确赋值。

3. PER 编码约束未满足

    uper_encode() 的调用依赖于 asn_per_constraints_t 和类型描述符 asn_TYPE_descriptor_t。
    如果约束不满足，编码会失败。需要检查：
        NR_CellGroupConfig 的 constraints 是否被正确设置。
        数据是否符合 PER 编码的格式要求。

4. 动态分配内存的错误

    如果某些指针未正确分配内存（如 rlc_BearerToAddModList），会导致 uper_encode 失败。
    检查所有动态分配的字段是否通过 calloc/malloc 正确分配，并确保 list.count 和 list.array 一致。

5. 添加调试日志

    在 encode_cellGroupConfig() 中打印 cellGroupConfig 的所有字段，确保没有为 NULL 的必填字段。
    添加断言或日志检查 rlc_BearerToAddModList 和其他关键结构体的内容。

示例调试代码：

if (!cellGroupConfig->rlc_BearerToAddModList || cellGroupConfig->rlc_BearerToAddModList->list.count == 0) {
    fprintf(stderr, "rlc_BearerToAddModList is NULL or empty!\n");
    return -1;
}
for (int i = 0; i < cellGroupConfig->rlc_BearerToAddModList->list.count; i++) {
    struct NR_RLC_BearerConfig *bearer = cellGroupConfig->rlc_BearerToAddModList->list.array[i];
    if (!bearer || !bearer->servedRadioBearer) {
        fprintf(stderr, "Invalid RLC Bearer Config at index %d\n", i);
        return -1;
    }
}

解决步骤

    验证 cellGroupConfig 初始化：
        确保 get_initial_cellGroupConfig() 返回的结构体正确，所有字段都被完整赋值。

    检查 rlc_BearerToAddModList：
        list.count > 0，且 list.array 内的每个元素都有效。
        检查 NR_RLC_BearerConfig 结构体的初始化。

    逐步缩小问题范围：
        如果怀疑是 rlc_BearerToAddModList 引发的问题，可以先将其置为空或简化，验证编码是否成功。
        逐步添加配置项，找出导致错误的具体字段。

    测试 ASN.1 编码工具链：
        确保你的 ASN.1 编码器与 NR_CellGroupConfig 的最新版本匹配。
        如果使用了定制的 ASN.1 编码规则，验证规则是否正确。

    添加更多日志和断言：
        在 uper_encode() 调用之前，打印 NR_CellGroupConfig 中的所有值。

最后建议

    问题核心在于输入结构体中的某个字段不符合 PER 编码规则，导致 uper_encode_to_buffer() 失败。
    通过调试逐步排除，重点检查 rlc_BearerToAddModList 和其他可选字段。
    如果排除数据问题，尝试更新或重新编译 ASN.1 编码器，确保工具链正确。

如果仍有问题，可以进一步提供 get_initial_cellGroupConfig() 的实现，以及 NR_RLC_BearerConfig 的具体内容，我可以协助你深入分析。





## 24-12-19 问题收录
- 调整了gNB的时隙资源，每个周期有20个时隙；
- 但是现在UE连不上了，因为时间戳同步不了：
```

```
- 经过找寻 openair3/NAS/TOOLS/ue_eurecom_test_sfr.conf 找到了UE的配置文件，倒是意外之戏，【发现UE的HPLMN与核心网的不同】，可能这有导致多UE的时候，UE注册不成功的原因？
- 但是UE配置文件这边没有关于TDD的配置，所以时间戳的问题，应该就是基站的问题。

这是明天的调查方向
```
（1）gNB 配置中的 TDD 时隙资源设置

如果你之前调整了 gNB 的 TDD 配置，可能未正确通知 UE 或配置不完整。你可以检查以下内容：

    TDD 时隙配置是否符合规范（如标准 3GPP TS 38.213 中的时隙定义）。
    gNB 的帧结构是否支持所定义的 TDD 配置。

```


## 24-12-19 问题收录
- 找到pdu会话建立请求发送的代码部分，正在解析他所发送信令的结构，看看要怎么塞我们的功能进去。
- smf和amf网元的镜像要换成我们自己的。
- 找到imsi要怎么塞进去。


- g_options.count = utils::ParseInt(opt.getOption(itemCount)); 数量提取
- opt.getOption(itemImsi); IMSI提取
-     if (opt.hasFlag(itemImsi))
    {
        g_options.imsi = opt.getOption(itemImsi);
        if (g_options.imsi.length() > 5 && g_options.imsi[0] == 'i' && g_options.imsi[1] == 'm' &&
            g_options.imsi[2] == 's' && g_options.imsi[3] == 'i' && g_options.imsi[4] == '-')
        {
            g_options.imsi = g_options.imsi.substr(5);
        }

        Supi::Parse("imsi-" + g_options.imsi); // validate the string by parsing
        //注意
    }

- {"sim-inserted", m_base->nasTask->mm->m_usim->isValid()}, 

- void NasMm::onStart(NasSm *sm, Usim *usim) 

-     Usim *m_usim; 
- {"ecall-only", ::ToJson(m_base->nasTask->usim->m_isECallOnly)}, //注意

- namespace nr::ue
{

class Usim
{
  private:
    bool m_isValid{};

  public:
    // Security related
    std::unique_ptr<NasSecurityContext> m_currentNsCtx{};
    std::unique_ptr<NasSecurityContext> m_nonCurrentNsCtx{};
    OctetString m_rand{};
    OctetString m_resStar{};
    std::unique_ptr<SqnManager> m_sqnMng{};

    // Others
    bool m_isECallOnly = false;   // todo: configurable
    bool m_emgIndication = false; // todo: configurable

  public:
    void initialize(bool hasSupi);

    bool isValid();
    void invalidate();
};

} // namespace nr::ue





## 24-12-23 问题收录
- 我现在想引入ueId到register.cpp的文件里，用于到时候索引didserver，但是现在一直报错
- 我用的是全局变量的方法
在 connection.cpp 中定义全局变量：

// src/gnb/rrc/connection.cpp

#include "connection.hpp"  // 包含头文件

int g_ueId = -1;  // 定义并初始化全局变量 g_ueId


在 connection.hpp 中声明全局变量：

// src/gnb/rrc/connection.hpp

#pragma once

extern int g_ueId;  // 使用 extern 声明全局变量 g_ueId


// src/ue/nas/mm/register.cpp

#include <gnb/rrc/connection.hpp>  // 引入 connection.hpp

void some_function() {
    // 现在你可以使用 g_ueId
    printf("The current UE ID is: %d\n", g_ueId);
}





“249.3 make[3]: Entering directory '/UERANSIM/cmake-build-release'
249.4 make[3]: Leaving directory '/UERANSIM/cmake-build-release'
249.4 make[3]: Entering directory '/UERANSIM/cmake-build-release'
249.4 [ 99%] Building CXX object CMakeFiles/nr-ue.dir/src/ue.cpp.o
252.0 [ 99%] Linking CXX executable nr-ue
252.2 src/ue/libue.a(register.cpp.o): In function nr::ue::NasMm::receiveInitialRegistrationAccept(nas::RegistrationAccept const&)':
252.2 register.cpp:(.text+0x7212): undefined reference to g_ueId'
252.2 collect2: error: ld returned 1 exit status
252.2 make[3]: *** [nr-ue] Error 1
252.2 CMakeFiles/nr-ue.dir/build.make:104: recipe for target 'nr-ue' failed
252.2 make[3]: Leaving directory '/UERANSIM/cmake-build-release'
252.2 make[2]: *** [CMakeFiles/nr-ue.dir/all] Error 2
252.2 CMakeFiles/Makefile2:269: recipe for target 'CMakeFiles/nr-ue.dir/all' failed
252.2 make[2]: Leaving directory '/UERANSIM/cmake-build-release'
252.2 Makefile:90: recipe for target 'all' failed
252.2 make[1]: Leaving directory '/UERANSIM/cmake-build-release'
252.2 make[1]: *** [all] Error 2
252.2 makefile:5: recipe for target 'build' failed
252.2 make: Leaving directory '/UERANSIM'
252.2 make: *** [build] Error 2”




## 24-12-25 问题收录
193.7 /UERANSIM/src/ue/nas/mm/register.cpp:18:10: fatal error: curl/curl.h: No such file or directory
193.7  #include <curl/curl.h>
193.7           ^~~~~~~~~~~~~
193.7 compilation terminated.

- 下一步就是把response提取出来DID，然后发送到核心网，再解密出来




## 25-01-13 问题收录
186.5 [ 96%] Building CXX object src/ue/CMakeFiles/ue.dir/nas/mm/proc.cpp.o
187.9 [ 96%] Building CXX object src/ue/CMakeFiles/ue.dir/nas/mm/radio.cpp.o
189.6 [ 96%] Building CXX object src/ue/CMakeFiles/ue.dir/nas/mm/register.cpp.o
189.7 /UERANSIM/src/ue/nas/mm/register.cpp:18:10: fatal error: curl/curl.h: No such file or directory
189.7  #include <curl/curl.h>
189.7           ^~~~~~~~~~~~~
189.7 compilation terminated.
189.7 make[3]: *** [src/ue/CMakeFiles/ue.dir/nas/mm/register.cpp.o] Error 1
189.7 src/ue/CMakeFiles/ue.dir/build.make:271: recipe for target 'src/ue/CMakeFiles/ue.dir/nas/mm/register.cpp.o' failed
189.7 make[3]: Leaving directory '/UERANSIM/cmake-build-release'
189.7 make[2]: *** [src/ue/CMakeFiles/ue.dir/all] Error 2
189.7 CMakeFiles/Makefile2:548: recipe for target 'src/ue/CMakeFiles/ue.dir/all' failed
189.7 make[2]: Leaving directory '/UERANSIM/cmake-build-release'
189.7 make[1]: *** [all] Error 2
189.7 Makefile:90: recipe for target 'all' failed
189.7 make[1]: Leaving directory '/UERANSIM/cmake-build-release'
189.7 make: *** [build] Error 2
189.7 makefile:5: recipe for target 'build' failed
189.7 make: Leaving directory '/UERANSIM'
------

 2 warnings found (use --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 4)
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 28)
Dockerfile.ubuntu.18.04:23
--------------------
  21 |     COPY src/ /UERANSIM/src/
  22 |     
  23 | >>> RUN make -C UERANSIM
  24 |     
  25 |     #---------------------------------------------------------------------
--------------------
ERROR: failed to solve: process "/bin/sh -c make -C UERANSIM" did not complete successfully: exit code: 2


## 25-01-16 
gpt劝我在cmakelist加上这些，但我先试试只加这些把

include_directories(/usr/include/x86_64-linux-gnu/curl)
target_link_libraries(nr-ue curl)


target_link_libraries(nr-ue
    pthread
    dl
    z
    ssl
    crypto
    nghttp2
    idn2
    rtmp
    psl
    curl
)


## 25-01-27
现在还是回到dpu会话这边来实现did功能了；

struct PduSessionEstablishmentRequest : SmMessage
{
    IEIntegrityProtectionMaximumDataRate integrityProtectionMaximumDataRate{};
    std::optional<IEPduSessionType> pduSessionType{};
    std::optional<IESscMode> sscMode{};
    std::optional<IE5gSmCapability> smCapability{};
    std::optional<IEMaximumNumberOfSupportedPacketFilters> maximumNumberOfSupportedPacketFilters{};
    std::optional<IEAlwaysOnPduSessionRequested> alwaysOnPduSessionRequested{};
    std::optional<IESmPduDnRequestContainer> smPduDnRequestContainer{};
    std::optional<IEExtendedProtocolConfigurationOptions> extendedProtocolConfigurationOptions{};

    std:optional<std::string> did{}; //DID fields

    PduSessionEstablishmentRequest();
    void onBuild(NasMessageBuilder &b);
};

void PduSessionEstablishmentRequest::onBuild(NasMessageBuilder &b)
{
    b.mandatoryIE(&integrityProtectionMaximumDataRate);
    b.optionalIE1(0x9, &pduSessionType);
    b.optionalIE1(0xA, &sscMode);
    b.optionalIE(0x28, &smCapability);
    b.optionalIE(0x55, &maximumNumberOfSupportedPacketFilters);
    b.optionalIE1(0xB, &alwaysOnPduSessionRequested);
    b.optionalIE(0x39, &smPduDnRequestContainer);
    b.optionalIE(0x7B, &extendedProtocolConfigurationOptions);
    
    if (did.has_value()) {
        b.optionalIE(0x7C, did.value());
        }
    }

did



# UE改造记录（UE的DID生成部分）

1. src/ue/nas/sm/establishment.cpp 180行
```
    /* DID function realization */
    std::string imsi_str = m_base->config->supi.value().value;
    printf("m_base->config->supi: %s\n",imsi_str.c_str());
    long long imsi_ll = std::stoll(imsi_str);
    printf("imsi_ll: %lld\n", imsi_ll);
    int ue_num = imsi_ll - 208950000000031 ;
    int initial_didserver = 8080;

    int didserver = initial_didserver + ue_num ;
    printf("This UE's didserver port:%d\n", didserver);

    //send imsi to didserver
    std::string response = send_imsi_to_didserver(imsi_str, didserver);
    printf("DID document is: %s\n",response.c_str());

```

2. src/lib/nas/msg.hpp 354行
```
struct PduSessionEstablishmentRequest : SmMessage
{
    IEIntegrityProtectionMaximumDataRate integrityProtectionMaximumDataRate{};
    std::optional<IEPduSessionType> pduSessionType{};
    std::optional<IESscMode> sscMode{};
    std::optional<IE5gSmCapability> smCapability{};
    std::optional<IEMaximumNumberOfSupportedPacketFilters> maximumNumberOfSupportedPacketFilters{};
    std::optional<IEAlwaysOnPduSessionRequested> alwaysOnPduSessionRequested{};
    std::optional<IESmPduDnRequestContainer> smPduDnRequestContainer{};
    std::optional<IEExtendedProtocolConfigurationOptions> extendedProtocolConfigurationOptions{};

    std::optional<IEdid> did{}; //DID fields

    PduSessionEstablishmentRequest();
    void onBuild(NasMessageBuilder &b);
};
```

3. src/lib/nas/msg.cpp 338行
```
void PduSessionEstablishmentRequest::onBuild(NasMessageBuilder &b)
{
    b.mandatoryIE(&integrityProtectionMaximumDataRate);
    b.optionalIE1(0x9, &pduSessionType);
    b.optionalIE1(0xA, &sscMode);
    b.optionalIE(0x28, &smCapability);
    b.optionalIE(0x55, &maximumNumberOfSupportedPacketFilters);
    b.optionalIE1(0xB, &alwaysOnPduSessionRequested);
    b.optionalIE(0x39, &smPduDnRequestContainer);
    b.optionalIE(0x7B, &extendedProtocolConfigurationOptions);
    
    if (did.has_value()) {
        b.optionalIE(0x7C, &did);
        }
}
```

4. src/lib/nas/ie1.hpp 186行
```
struct IEdid : InformationElement2
{
    std::string did;

    IEdid() = default;
    explicit IEdid(const std::string &did) : did(did) {}

    static IEdid Decode(const std::string &str)
    {
        return IEdid(str);
    }

    static std::string Encode(const IEdid &ie)
    {
        return ie.did;
    }
};
```


5. src/ue/nas/sm/establishment.cpp
```
#include <utils/options.hpp>
#include <utils/common.hpp>
#include <iostream>
#include <string>
#include <curl/curl.h>

namespace nr::ue
{

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t total_size = size * nmemb;
    std::string* response = reinterpret_cast<std::string*>(userp);
    response->append(reinterpret_cast<char*>(contents), total_size);
    return total_size;
}

std::string send_imsi_to_didserver(const std::string& imsi, int didserver){
    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if (curl) {
        std::string url = "http://localhost:" + std::to_string(didserver) + "/hello";
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "http");

        struct curl_slist *headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        std::string data = "{\n\"IMSI\" : \"" + imsi + "\"\n}";

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());

        std::string response_data;
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "CURL failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Response from server: " << response_data << std::endl;

            std::cout << "Received IMSI from server: " << response_data << std::endl;
        }

        curl_easy_cleanup(curl);

        return response_data;

    }
    curl_global_cleanup();
}


void NasSm::sendEstablishmentRequest(const SessionConfig &config)
{
    m_logger->debug("Sending PDU Session Establishment Request");

    /* Control the protocol state */
    if (m_mm->m_rmState != ERmState::RM_REGISTERED)
    {
        m_logger->err("PDU session establishment could not be triggered, UE is not registered");
        return;
    }

    if (m_mm->m_mmSubState == EMmSubState::MM_REGISTERED_NON_ALLOWED_SERVICE && !m_mm->hasEmergency() &&
        !m_mm->isHighPriority())
    {
        m_logger->err("PDU session establishment could not be triggered, non allowed service condition");
        return;
    }

    /* Control the received config */
    if (config.type != nas::EPduSessionType::IPV4)
    {
        m_logger->err("PDU session type [%s] is not supported", nas::utils::EnumToString(config.type));
        return;
    }
    if (m_mm->m_rmState == ERmState::RM_REGISTERED && m_mm->m_registeredForEmergency && !config.isEmergency)
    {
        m_logger->err("Non-emergency PDU session cannot be requested, UE is registered for emergency only");
        return;
    }
    if (config.isEmergency && anyEmergencySession())
    {
        m_logger->err(
            "Emergency PDU session cannot be requested, another emergency session already established or establishing");
        return;
    }

    /* Allocate PSI */
    int psi = allocatePduSessionId(config);
    if (psi == 0)
        return;

    /* Allocate PTI */
    int pti = allocateProcedureTransactionId();
    if (pti == 0)
    {
        freePduSessionId(psi);
        return;
    }

    /* Set relevant fields of the PS description */
    auto &ps = m_pduSessions[psi];
    ps->psState = EPsState::ACTIVE_PENDING;
    ps->sessionType = config.type;
    ps->apn = config.apn;
    ps->sNssai = config.sNssai;
    ps->isEmergency = config.isEmergency;
    ps->authorizedQoSRules = {};
    ps->sessionAmbr = {};
    ps->authorizedQoSFlowDescriptions = {};
    ps->pduAddress = {};
    ps->uplinkPending = false;

    /* Make PCO */
    nas::ProtocolConfigurationOptions opt{};
    opt.additionalParams.push_back(std::make_unique<nas::ProtocolConfigurationItem>(
        nas::EProtocolConfigId::CONT_ID_UP_IP_ADDRESS_ALLOCATION_VIA_NAS_SIGNALLING, true, OctetString::Empty()));
    opt.additionalParams.push_back(std::make_unique<nas::ProtocolConfigurationItem>(
        nas::EProtocolConfigId::CONT_ID_DOWN_DNS_SERVER_IPV4_ADDRESS, true, OctetString::Empty()));

    nas::IEExtendedProtocolConfigurationOptions iePco{};
    iePco.configurationProtocol = nas::EConfigurationProtocol::PPP;
    iePco.extension = true;
    iePco.options = opt.encode();

    /* Prepare the establishment request message */
    auto req = std::make_unique<nas::PduSessionEstablishmentRequest>();
    req->pti = pti;
    req->pduSessionId = psi;
    req->integrityProtectionMaximumDataRate = MakeIntegrityMaxRate(m_base->config->integrityMaxRate);
    req->pduSessionType = nas::IEPduSessionType{};
    req->pduSessionType->pduSessionType = nas::EPduSessionType::IPV4;
    req->sscMode = nas::IESscMode{};
    req->sscMode->sscMode = nas::ESscMode::SSC_MODE_1;
    req->extendedProtocolConfigurationOptions = std::move(iePco);
    req->smCapability = MakeSmCapability();

    /* DID function realization */
    std::string imsi_str = m_base->config->supi.value().value;
    printf("m_base->config->supi: %s\n", imsi_str.c_str());
    long long imsi_ll = std::stoll(imsi_str);
    printf("imsi_ll: %lld\n", imsi_ll);
    int ue_num = imsi_ll - 208950000000031;
    int initial_didserver = 8081;

    int didserver = initial_didserver + ue_num;
    printf("This UE's didserver port:%d\n", didserver);
    
    // obtain the time
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
        now.time_since_epoch()
    ) % 1000000;
    // transfer the time form
    std::tm tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
    
    // to time str
    char buffer1[80];
    std::strftime(buffer1, sizeof(buffer1), "%Y-%m-%d %H:%M:%S", &tm);
    
    // logs in the txt
    std::ofstream file("timelogs.txt", std::ios::app);
    if (file) {
        file << "UE发送IMSI时间: " << buffer1 << "." 
            << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
    }
    
    // send imsi to didserver
    std::string response = send_imsi_to_didserver(imsi_str, didserver);

    time = std::chrono::system_clock::to_time_t(now);
    microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
        now.time_since_epoch()
    ) % 1000000;
    // transfer the time form
    tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
    
    // to time str
    char buffer2[80];
    std::strftime(buffer2, sizeof(buffer2), "%Y-%m-%d %H:%M:%S", &tm);
    
    // logs in the txt

    if (file) {
        file << "接受did时间: " << buffer2 << "." 
            << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
    }

    if (!response.empty()) {
    // printf("DID document is: %s\n",response.c_str());
    std::cout << "Received DID from server: " << response << std::endl;

    std::string did = extractDID(response);
    std::cout << "Extracted DID: " << did << std::endl;

    // std::string hex_did = stringToHex(response);
    // std::cout << "Hex DID: " << hex_did << std::endl;

    // req->did = nas::IEdid(response);
    req->did = nas::IEdid(did);
    }

    // req->did = nas::IEdid(hex_did);

    /* Set relevant fields of the PT, and start T3580 */
    auto &pt = m_procedureTransactions[pti];
    pt.state = EPtState::PENDING;
    pt.timer = newTransactionTimer(3580);
    pt.message = std::move(req);
    pt.psi = psi;

    /* Send SM message */
    sendSmMessage(psi, *pt.message);
}

```

6. src/gnb/rrc/sap.cpp

```

#include <fstream>
#include <chrono>
#include <iomanip>
#include <ctime>

namespace nr::gnb
{

void GnbRrcTask::handleRlsSapMessage(NmGnbRlsToRrc &msg)
{
    switch (msg.present)
    {
    case NmGnbRlsToRrc::SIGNAL_DETECTED: {
        m_logger->debug("UE[%d] new signal detected", msg.ueId);
        triggerSysInfoBroadcast();
        
    
            // 获取带微秒的当前时间
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
            now.time_since_epoch()
        ) % 1000000;
        // 转换成本地时间格式
        std::tm tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
        
        // 格式化时间字符串
        char buffer[80];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        
        // 追加写入文件
        std::ofstream file("timelogs.txt", std::ios::app);
        if (file) {
            file << "UE启动的时间: " << buffer << "." 
                << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
        }


        break;
    }
    case NmGnbRlsToRrc::UPLINK_RRC: {
        handleUplinkRrc(msg.ueId, msg.rrcChannel, msg.data);
        break;
    }
    }
}

} // namespace nr::gnb
```

7. docker/Dockerfile.ubuntu.18.04:
```
FROM ubuntu:bionic as ueransim

RUN apt-get update && apt-get install -y tzdata
# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone  # 同步写入 timezone 文件


RUN apt update && apt install -y iproute2 iputils-ping net-tools\
    iperf3 libsctp-dev lksctp-tools libcurl4-openssl-dev
# RUN dpkg-query -L libcurl4-openssl-dev && ldconfig
# RUN dpkg-query -L libcurl4-openssl-dev | tee /tmp/curl_libs.log && \
#     cat /tmp/curl_libs.log && ldconfig




WORKDIR /ueransim/etc
COPY --from=ueransim-builder /UERANSIM/docker/custom*.yaml  /ueransim/etc/

WORKDIR /ueransim/bin
COPY --from=ueransim-builder /UERANSIM/build/*  /ueransim/bin/
COPY --from=ueransim-builder /UERANSIM/docker/entrypoint.sh . 

ENTRYPOINT ["/ueransim/bin/entrypoint.sh"]
```



# 核心网接受did工作开始



## 25-2-13工作记录

现在要首先确定did在nas中是否被正确编码，其次确定如何在amf中解析出来。

1. 在 nas::EncodeNasMessage 里添加日志

在 nas::EncodeNasMessage 方法内部，增加日志输出，确认 msg 是否包含 DID，并且 DID 是否被成功编码进 m.payloadContainer.data。

例如：

void EncodeNasMessage(const nas::SmMessage &msg, bstring &encoded)
{
    Logger::nas().debug("Encoding NAS Message Type: %d", static_cast<int>(msg.messageType));

    if (msg.messageType == nas::EMessageType::PDU_SESSION_ESTABLISHMENT_REQUEST)
    {
        auto *pduRequest = dynamic_cast<const nas::PduSessionEstablishmentRequest *>(&msg);
        if (pduRequest)
        {
            Logger::nas().debug("Encoding PDU Session Establishment Request with DID: %s", 
                                pduRequest->did.has_value() ? pduRequest->did->value().c_str() : "No DID");

            // 确保 DID 被正确序列化进 encoded
        }
    }

    // 原有的编码逻辑...
}

然后在 AMF 端的日志中，看看 DID 是否正确输出。
2. 检查 nas::PduSessionEstablishmentRequest 结构体

确认 nas::PduSessionEstablishmentRequest 结构体是否已经支持 DID 这一字段的序列化：

class PduSessionEstablishmentRequest : public SmMessage
{
public:
    IEIntegrityProtectionMaximumDataRate integrityProtectionMaximumDataRate;
    IEPduSessionType pduSessionType;
    IESscMode sscMode;
    IEDid did;  // 你的 DID 字段
    // 其他字段...

    virtual bool Encode(bstring &data) const override;
};

然后，在 Encode() 方法里确保 did 被正确添加到 data 中：

bool PduSessionEstablishmentRequest::Encode(bstring &data) const
{
    Logger::nas().debug("Encoding PDU Session Establishment Request");

    // 序列化常规字段...
    
    if (did.has_value())
    {
        Logger::nas().debug("Adding DID to NAS message: %s", did->value().c_str());
        AppendToBstring(data, did->value());  // 确保 DID 被正确写入 data
    }

    return true;
}

3. 在 AMF 端解码 DID

在 AMF 端解析 NAS 消息的地方，确保 DID 能正确解析出来：

std::string extracted_did;
if (nasMessage->did.has_value())
{
    extracted_did = nasMessage->did->value();
    Logger::amf_n1().debug("Extracted DID from NAS message: %s", extracted_did.c_str());
}



最终修改代码
1. AMF 解析 DID 并存储

// AMF解析DID
std::string extract_did_from_nas_message(bstring sm_msg) {
    // 解析SM_MSG并提取DID
    std::string did = ""; 
    // TODO: 实现DID提取逻辑
    return did;
}

在 handle_pdu_session_initial_request 里：

psc->did = extract_did_from_nas_message(sm_msg);

2. 在 pdu_session_establishment_request 里添加 DID

pdu_session_establishment_request["DID"] = psc->did.c_str();


## 25-2-17工作记录
现在有两个选择，关于核心网解析did的方法：
1. 重新跑一下过去的代码，试着分析一下阿迪的操作办法（编译老核心网元，启动区块链，看amf网元）
2. 分析pdu会话编码的代码，看看怎么解析？因为阿迪那个虽然能知道咋做，我依然要看这边的代码，看看和不合适

## 25-2-18工作记录 - 寻找DID编码失败的原因
这段代码定义了一个结构体 NasMessageBuilder，它主要用于管理编码和解码过程中所需要的编码器和解码器。这个结构体包含了针对“必需（mandatory）”和“可选（optional）”信息元素（IEs，Information Elements）的编码和解码器的管理功能。
结构体解释

    成员变量：
        mandatoryEncoders 和 optionalEncoders：分别存储必需和可选信息元素的编码器。这些编码器是函数对象，接受 OctetString & 类型的参数，并将数据编码到字节流中。
        mandatoryDecoders 和 optionalDecoders：分别存储必需和可选信息元素的解码器。这些解码器是函数对象，接受 OctetView & 类型的参数，并从字节流中解码数据。

    模板函数： 这些模板函数（如 mandatoryIE, optionalIE 等）提供了一种通用的方法来添加信息元素（IEs）的编码和解码规则。它们通过推导出具体类型 T 或 U，并根据需要将编码和解码操作添加到 mandatoryEncoders 和 optionalEncoders 中。

1. mandatoryIE 和 mandatoryIE1
mandatoryIE：

template <typename T>
inline void mandatoryIE(T *ptr)
{
    mandatoryEncoders.push_back([ptr](OctetString &stream) { Encode2346(*ptr, stream); });
    mandatoryDecoders.push_back([ptr](const OctetView &stream) { *ptr = DecodeIe2346<T>(stream); });
}

    作用：这个模板函数用来添加一个必需信息元素（IE）的编码和解码规则。具体来说：
        编码规则：使用 Encode2346 函数编码 ptr 指向的数据，编码结果存入 stream。
        解码规则：从 stream 中解码数据，并将解码后的结果存入 ptr。

mandatoryIE1：

template <typename T>
inline void mandatoryIE1(T *ptr)
{
    mandatoryEncoders.push_back([ptr](OctetString &stream) { EncodeIe1(0, *ptr, stream); });
    mandatoryDecoders.push_back([ptr](const OctetView &stream) { *ptr = DecodeIe1<T>(stream); });
}

    作用：这个函数类似于 mandatoryIE，但它使用了 EncodeIe1 和 DecodeIe1 函数，可能是为了对信息元素进行特定的编码（例如，添加了额外的标识符 0）。

mandatoryIE1 (两个参数版本)：

template <typename T, typename U>
inline void mandatoryIE1(T *ptr1, U *ptr2)
{
    mandatoryEncoders.push_back([ptr1, ptr2](OctetString &stream) { EncodeIe1(*ptr1, *ptr2, stream); });
    mandatoryDecoders.push_back([ptr1, ptr2](const OctetView &stream) {
        int octet = stream.readI();
        *ptr1 = T::Decode((octet >> 4) & 0xF);
        *ptr2 = U::Decode(octet & 0xF);
    });
}

    作用：这个函数用于两个参数类型的信息元素。编码时，它调用 EncodeIe1 函数并传递两个参数。解码时，首先从流中读取一个字节，然后将其分解为两个部分，分别解码到 ptr1 和 ptr2 中。

2. optionalIE 和 optionalIE1
optionalIE：

template <typename T>
inline void optionalIE(int iei, std::optional<T> *ptr)
{
    optionalEncoders.push_back([ptr, iei](OctetString &stream) {
        if (ptr->has_value())
        {
            stream.appendOctet(iei);
            Encode2346(ptr->value(), stream);
        }
    });
    optionalDecoders[iei] = [ptr](const OctetView &stream) {
        stream.readI();
        *ptr = DecodeIe2346<T>(stream);
    };
}

    作用：这个函数用于处理可选的信息元素（IE）。它会检查 ptr 是否包含值（has_value()），如果包含，则将 iei 和信息元素的编码结果添加到 stream 中。对于解码，它会首先读取 iei，然后解码出信息元素。

optionalIE1：

template <typename T>
inline void optionalIE1(int iei, std::optional<T> *ptr)
{
    optionalEncoders.push_back([ptr, iei](OctetString &stream) {
        if (ptr->has_value())
            EncodeIe1(iei, ptr->value(), stream);
    });
    optionalDecoders[iei] = [ptr](const OctetView &stream) { *ptr = DecodeIe1<T>(stream); };
}

    作用：与 optionalIE 类似，但使用了 EncodeIe1 和 DecodeIe1 函数。

3. 总结

    必需信息元素（Mandatory Information Elements）：通过 mandatoryIE 和 mandatoryIE1 函数进行编码和解码。它们将信息元素添加到 mandatoryEncoders 和 mandatoryDecoders 中。

    可选信息元素（Optional Information Elements）：通过 optionalIE 和 optionalIE1 函数进行编码和解码。如果 optional 类型的信息元素有值，则会编码到流中；如果没有值，编码将被跳过。

4. DID 编码失败的潜在原因

从这段代码来看，编码的核心操作都在这些 Encode 函数中。如果 DID 编码失败，可能是因为：

    DID 编码器未添加到 mandatoryEncoders 或 optionalEncoders 中。你可以检查 DID 字段是否通过 mandatoryIE 或 optionalIE 等函数正确地被添加到了 builder 中。

    信息元素类型不匹配。例如，DID 可能在某些编码操作中被期望作为 std::optional<std::string> 类型，而实际可能没有进行类型匹配。检查 DID 字段的类型定义以及它的编码/解码方式。

    Encode2346 和 EncodeIe1 等编码函数的实现问题。这些函数可能没有正确处理 DID 的编码。你可以进一步排查这些具体的编码函数。

5. 排查建议

    确保在构建消息时，DID 字段使用了适当的编码规则，并添加到了 mandatoryEncoders 或 optionalEncoders 中。
    如果是可选的 DID 字段，确保它在消息构建过程中已经赋值并正确编码。
    调试时可以检查 stream 内容，确保在编码过程中确实有正确的字节流生成。



## 25-2-20工作记录 - UE部分DID已经编码成功，现在看如何给核心网这边提取出来
从你的日志和代码中可以看出，你的目标是从核心网收到的字节流中提取并解析出 `DID` 字段。我们看到的日志显示了 PDU 会话的编码，其中包含了 `7C`，它是 `DID` 编码的一部分。

在核心网的代码中，你希望提取 `DID` 字段并进行处理。以下是对如何在核心网代码中解析和处理这个 `DID` 字段的一些思考。

### 关键思路

1. **日志输出的分析**：
   日志显示的编码 `Buffer: 2e0101c1ffff91a12801007b000780000a00000d007c4449443a494d53493a633330613130373833396363373336373662643061323564663838383133393662646331323163333764383638383366623433316431326461303938613164363136646633663563663837323837653362613864623035633061313634333738326364663461376666346236356534383861623065656265323565653838333830`，其中 `7C` 字节似乎对应 `DID` 编码的开始。

2. **提取 `DID`**：
   - 从日志中可以看出，`DID` 字符串是以 `DID:IMSI:` 为前缀的，接下来是一个较长的十六进制字符串。`7C` 是你提到的编码部分，可能指示 `DID` 开始的位置。
   - 要从字节流中提取 `DID` 字符串，你需要解码这部分数据并提取出 `DID` 作为字符串。

3. **解析字节流**：
   - 你已经有一个函数 `octet_stream_2_hex_stream()`，这个函数将字节流转换为十六进制字符串。接下来，你需要解析这些字节，找出 `DID` 字符串的位置。

### 如何提取 `DID`

1. **字节流解析**：
   - 你收到的字节流可能是以某种格式（例如 UTF-8 或自定义编码）编码的。`7C` 字节作为标记，可能表示 `DID` 的起始位置或是某个特定字段的标志。
   - 你需要从字节流中找到 `7C` 字节所在的位置，然后提取该位置后的内容，直到解析出完整的 `DID` 字符串。

2. **修改 `handle_pdu_session_initial_request` 函数**：
   你可以在 `handle_pdu_session_initial_request` 函数中添加一个步骤，从 `sm_msg`（即字节流消息）中解析出 `DID`。

   示例代码：
   ```cpp
   void amf_sbi::handle_pdu_session_initial_request(
       const std::string& supi, std::shared_ptr<pdu_session_context>& psc,
       const std::string& smf_uri_root, const std::string& smf_api_version,
       bstring sm_msg, const std::string& dnn) {

       Logger::amf_sbi().debug(
           "Handle PDU Session Establishment Request (SUPI %s, PDU Session ID %d)",
           supi.c_str(), psc->pdu_session_id);

       // Step 1: Parse DID from the buffer
       std::string n1sm_msg = {};
       octet_stream_2_hex_stream(
           (uint8_t*) bdata(sm_msg), blength(sm_msg), n1sm_msg);

       // Step 2: Find the DID string in the encoded message (using the byte index or delimiter)
       size_t did_start_pos = n1sm_msg.find("DID:IMSI:");  // Look for DID prefix in the hex string
       if (did_start_pos != std::string::npos) {
           std::string did = n1sm_msg.substr(did_start_pos);  // Extract the DID part
           Logger::amf_sbi().debug("Extracted DID: %s", did.c_str());
       } else {
           Logger::amf_sbi().error("DID not found in the encoded message");
       }

       // Continue processing the request
       nlohmann::json pdu_session_establishment_request;
       pdu_session_establishment_request["supi"] = supi.c_str();
       // Add other fields...
   }
   ```

### 解释：

1. **提取 `DID`**：
   - 在解析 `n1sm_msg` 时，我们通过 `find()` 函数查找 `DID:IMSI:` 前缀的位置。然后，使用 `substr()` 提取从该位置开始的字符串，这部分字符串就是 `DID`。

2. **日志记录**：
   - 如果找到 `DID`，就通过日志记录输出。如果没有找到 `DID`，则记录错误日志。

3. **继续处理请求**：
   - 提取 `DID` 后，你可以继续处理 PDU 会话建立请求，将 `DID` 和其他必要的信息加入到请求中并发送。

### 总结

- **目标**：解析字节流中的 `DID` 字符串，通常通过找到 `DID:IMSI:` 或类似的前缀来定位。
- **提取方法**：在收到的字节流中查找特定字段或标志（如 `7C` 或 `DID:IMSI:` 前缀），然后提取出后续内容。
- **核心思路**：通过 `find()` 和 `substr()` 来定位并提取 `DID` 字符串。

如果你有更详细的协议或字节流结构信息，可以进一步优化这个解析过程。



## 25-2-23日记录
核心网已经收到编码了，能够确定
component/oai-amf/src/amf-app/amf_n1.cpp的
```
void amf_n1::ul_nas_transport_handle(
    const uint32_t ran_ue_ngap_id, const long amf_ue_ngap_id, bstring nas,
    const plmn_t& plmn) {
  // Decode UL_NAS_TRANSPORT message
  Logger::amf_n1().debug("Handling UL NAS Transport");
  auto ul_nas = std::make_unique<UlNasTransport>();
  ul_nas->Decode((uint8_t*) bdata(nas), blength(nas));

```
这个部分已经对他进行了解码，但是解码的顺序很离奇，跳过了DID：IMSI 开头的 0x44，直接从末尾的0x12开始的，不知道他的逻辑是怎么样的？现在我对nas的这个bstring进行了输出，可以确定nas本身没有问题。
也就是decode这个代码包含的

```
int UlNasTransport::Decode(uint8_t* buf, int len) {
  Logger::nas_mm().debug("Decoding UlNasTransport message");
  int decoded_size    = 0;
  int decoded_ie_size = 0;

  // Header
  decoded_ie_size = NasMmPlainHeader::Decode(buf, len);
  if (decoded_ie_size == KEncodeDecodeError) {
    Logger::nas_mm().error("Decoding NAS Header error");
    return KEncodeDecodeError;
  }
  decoded_size += decoded_ie_size;

  // Payload Container Type
  if ((decoded_ie_size = NasHelper::Decode(
           ie_payload_container_type, buf, len, decoded_size, false)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }
  if (decoded_ie_size == 0)
    decoded_size++;  // 1/2 octet for PayloadContainerType, 1/2 octet for spare

  // Payload Container
  // TODO: use NAS helper
  decoded_ie_size = ie_payload_container.Decode(
      buf + decoded_size, len - decoded_size, false,
      ie_payload_container_type.GetValue());
  if (decoded_ie_size == KEncodeDecodeError) {
    Logger::nas_mm().error(
        "Decoding %s error", PayloadContainer::GetIeName().c_str());
    return KEncodeDecodeError;
  }
  decoded_size += decoded_ie_size;

  Logger::nas_mm().debug("Decoded_size (%d)", decoded_size);

  // Decode other IEs
  uint8_t octet = 0x00;
  DECODE_U8_VALUE(buf + decoded_size, octet);
  Logger::nas_mm().debug("First option IEI (0x%x)", octet);
  bool flag = false;

  while ((octet != 0x0)) {
    switch ((octet & 0xf0) >> 4) {
```
阿迪曾经也是在这里进行了操作。




## 25-2-25日 工作记录
component/oai-amf/src/nas/msgs/UlNasTransport.cpp：

void UlNasTransport::GetPayloadContainer(bstring& content) const {
  ie_payload_container.GetValue(content);
}

<!-- -------------------------------------------------  -->
component/oai-amf/src/nas/msgs/UlNasTransport.hpp：

#include "NasIeHeader.hpp"

namespace nas {

class UlNasTransport : public NasMmPlainHeader {
 public:
  UlNasTransport();
  ~UlNasTransport();

  void SetHeader(uint8_t security_header_type);

  int Encode(uint8_t* buf, int len);
  int Decode(uint8_t* buf, int len);

  void SetPayloadContainerType(uint8_t value);
  uint8_t GetPayloadContainerType() const;

  void SetPayloadContainer(const std::vector<PayloadContainerEntry>& content);
  void GetPayloadContainer(std::vector<PayloadContainerEntry>& content) const;
  void GetPayloadContainer(bstring& content) const;

  void SetPduSessionId(uint8_t value);
  bool GetPduSessionId(uint8_t& value) const;

  void SetOldPduSessionId(uint8_t value);
  bool GetOldPduSessionId(uint8_t& value) const;

  void SetRequestType(uint8_t value);
  bool GetRequestType(uint8_t& value) const;

  void SetSNssai(const SNSSAI_s& snssai);
  bool GetSNssai(SNSSAI_s& snssai) const;

  void SetDnn(const bstring& dnn);
  bool GetDnn(bstring& dnn) const;

  void SetAdditionalInformation(const bstring& value);
  // TODO: Get

  void SetMaPduSessionInformation(uint8_t value);
  // TODO: Get

  void SetReleaseAssistanceIndication(uint8_t value);
  // TODO: Get

 public:
  PayloadContainerType ie_payload_container_type;  // Mandatory
  PayloadContainer ie_payload_container;           // Mandatory

  std::optional<PduSessionIdentity2> ie_pdu_session_id;            // Optional
  std::optional<PduSessionIdentity2> ie_old_pdu_session_id;        // Optional
  std::optional<RequestType> ie_request_type;                      // Optional
  std::optional<SNssai> ie_s_nssai;                                // Optional
  std::optional<Dnn> ie_dnn;                                       // Optional
  std::optional<AdditionalInformation> ie_additional_information;  // Optional
  std::optional<MaPduSessionInformation>
      ie_ma_pdu_session_information;  // Optional
  std::optional<ReleaseAssistanceIndication>
      ie_release_assistance_indication;  // Optional
};
}  // namespace nas

<!-- --------------------------------------------------------------- -->
component/oai-amf/src/nas/ies/PayloadContainer.hpp：
namespace nas {
class PayloadContainer : Type6NasIe {
 public:
  PayloadContainer();
  PayloadContainer(uint8_t iei);
  PayloadContainer(const bstring& b);
  PayloadContainer(uint8_t iei, const bstring& b);
  PayloadContainer(const std::vector<PayloadContainerEntry>& content);
  PayloadContainer(
      const uint8_t iei, const std::vector<PayloadContainerEntry>& content);
  ~PayloadContainer();

  static std::string GetIeName() { return kPayloadContainerIeName; }

  // void setValue(uint8_t iei, uint8_t value);
  int Encode(uint8_t* buf, int len, uint8_t type);
  int Decode(uint8_t* buf, int len, bool is_iei, uint8_t type);

  void SetValue(const bstring& cnt);
  bool GetValue(bstring& cnt) const;

  void SetValue(const std::vector<PayloadContainerEntry>& content);
  bool GetValue(std::vector<PayloadContainerEntry>& content) const;

 private:
  std::optional<bstring> content;
  std::optional<std::vector<PayloadContainerEntry>> CONTENT;
};
}  // namespace nas

<!-- ----------------------------------------------------------- -->
component/oai-amf/src/nas/ies/PayloadContainer.cpp：

bool PayloadContainer::GetValue(bstring& cnt) const {
  if (content.has_value()) {
    cnt = content.value();
    return true;
  }
  return false;
}




<!-- ============================================== -->

[2025-02-25 15:08:47.623] [nas_mm] [debug] Extracted 9+64 byte encoded data:
bstring content: 4449443A494D53493A376131363634373037373665306338626365643039613065303064613739326366326631376630316231646366386333386264643863353835383261326634653534636262306661653265323561333633383836653239353332663039363237303431336236373262343734623238313332353637333233633866316134333930
[2025-02-25 14:25:04.394] [nas] [debug] UAC access attempt is allowed for identity[0], category[MO_sig]

已经能把这个buffer提取出来了，现在就是如何将这个buffer，重新变回DID的字符了。

DID:IMSI:7a166470776e0c8bced09a0e00da792cf2f17f01b1dcf8c38bdd8c58582a2f4e54cbb0fae2e25a363886e29532f096270413b672b474b28132567323c8f1a43900
DID:IMSI:7a166470776e0c8bced09a0e00da792cf2f17f01b1dcf8c38bdd8c58582a2f4e54cbb0fae2e25a363886e29532f096270413b672b474b28132567323c8f1a4390

%!(EXTRA string={"Id":"DID:IMSI:e5748d66ef100ed5876b65e27314a30dc898143681e4089869046922a794bc1e4e4a510c7a92dce71d27b1ddd50fd1ff2d35b71bb9bb1217f460a21dc582facd00","Pk":"041abe06ff5058cb115002731ef03ea3992cf6958163373d668110f5831cad14865d58ceb23d3f9384b50969a36a14983fcf9289425bdc32392a7dfadb5f4e16dd"})


<!-- ================================================ -->

# 核心网改造记录 （更新于25-03-10）  
- component/oai-amf/src/amf-app/amf_sbi.hpp
```
  //SetDID curl_http_client modified
  void curl_http_client_DID(
        const std::string& remote_uri, const std::string& method,
        const std::string& msg_body, nlohmann::json& response_json,
        uint32_t& response_code, const uint8_t& http_version);
```

- component/oai-amf/src/amf-app/amf_sbi.cpp
```
//curl_http_client for DID
void amf_sbi::curl_http_client_DID(
  const std::string& remote_uri, const std::string& method,
  const std::string& msg_body, nlohmann::json& response_json,
  uint32_t& response_code, const uint8_t& http_version) {
Logger::amf_sbi().info("Send HTTP message to %s", remote_uri.c_str());
Logger::amf_sbi().info("HTTP message Body: %s", msg_body.c_str());

uint32_t str_len = msg_body.length();
// char* body_data  = (char*) malloc(str_len + 1);
// memset(body_data, 0, str_len + 1);
// memcpy((void*) body_data, (void*) msg_body.c_str(), str_len);

curl_global_init(CURL_GLOBAL_ALL);
CURL* curl = curl_easy_init();

if (curl) {
  CURLcode res               = {};
  struct curl_slist* headers = nullptr;

  std::string content_type = "Content-Type: application/x-www-form-urlencoded";
  std::string form_body = "DID=" + msg_body;

  headers                  = curl_slist_append(headers, content_type.c_str());
  curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
  curl_easy_setopt(curl, CURLOPT_URL, remote_uri.c_str());

  if (method.compare("POST") == 0)
    curl_easy_setopt(curl, CURLOPT_HTTPPOST, 1);
  else if (method.compare("PATCH") == 0)
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PATCH");
  else if (method.compare("PUT") == 0)
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
  else if (method.compare("DELETE") == 0)
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
  else  // GET
    curl_easy_setopt(curl, CURLOPT_HTTPGET, 1);

  curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, CURL_TIMEOUT_MS);
  curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1);
  curl_easy_setopt(curl, CURLOPT_INTERFACE, amf_cfg.sbi.if_name.c_str());

  if (http_version == 2) {
    if (Logger::should_log(spdlog::level::debug))
      curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
    // we use a self-signed test server, skip verification during debugging
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    curl_easy_setopt(
        curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE);
  }

  // Response information.
  long httpCode = {0};
  std::unique_ptr<std::string> httpData(new std::string());
  std::unique_ptr<std::string> httpHeaderData(new std::string());

  // Hook up data handling function.
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &callback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, httpData.get());
  curl_easy_setopt(curl, CURLOPT_HEADERDATA, httpHeaderData.get());
  if ((method.compare("POST") == 0) or (method.compare("PATCH") == 0) or
      (method.compare("PUT") == 0)) {
    curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, msg_body.length());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, form_body.c_str());
  }

  res = curl_easy_perform(curl);
  curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);

  // get the response
  std::string response = *httpData.get();
  std::string resMsg   = {};
  bool is_response_ok  = true;
  Logger::amf_sbi().info("Get response with HTTP code (%ld)", httpCode);

  response_code = httpCode;

  if (static_cast<http_response_codes_e>(httpCode) ==
      http_response_codes_e::HTTP_RESPONSE_CODE_0) {
    Logger::amf_sbi().info(
        "Cannot get response when calling %s", remote_uri.c_str());
    // free curl before returning
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return;
  }

  if ((static_cast<http_response_codes_e>(httpCode) !=
       http_response_codes_e::HTTP_RESPONSE_CODE_200_OK) and
      (static_cast<http_response_codes_e>(httpCode) !=
       http_response_codes_e::HTTP_RESPONSE_CODE_201_CREATED) and
      (static_cast<http_response_codes_e>(httpCode) !=
       http_response_codes_e::HTTP_RESPONSE_CODE_204_NO_CONTENT)) {
    is_response_ok = false;

    if (response.size() < 1) {
      Logger::amf_sbi().info("There's no content in the response");
      response_json = {};
      return;
    }
  }

  try {
    response_json = nlohmann::json::parse(response);
  } catch (nlohmann::json::exception& e) {
    Logger::amf_sbi().info("Could not get JSON content from the response");
    response_json = {};
  }

  Logger::amf_sbi().info(
      "Get response with Json content: %s", response_json.dump().c_str());

  curl_slist_free_all(headers);
  curl_easy_cleanup(curl);
}

curl_global_cleanup();


}
```

- component/oai-amf/src/amf-app/amf_n1.cpp  
```
//DID content extraction
std::string bstringToString(const bstring& bstr) {
  
  const char* c_str = bstr2cstr(bstr, '\0');
  std::string result(c_str);  
  return result;
}

std::string hexToString(const std::string& hex) {
  std::string result;
  for (size_t i = 0; i < hex.length(); i += 2) {
      std::string byteString = hex.substr(i, 2);
      char byte = (char)(int)strtol(byteString.c_str(), nullptr, 16);
      result.push_back(byte);
  }
  return result;
}


//------------------------------------------------------------------------------
void amf_n1::ul_nas_transport_handle(
    const uint32_t ran_ue_ngap_id, const long amf_ue_ngap_id, bstring nas,
    const plmn_t& plmn) {
  // Decode UL_NAS_TRANSPORT message
  Logger::amf_n1().debug("Handling UL NAS Transport");
  auto ul_nas = std::make_unique<UlNasTransport>();
  ul_nas->Decode((uint8_t*) bdata(nas), blength(nas));

  // print_bstring(nas);

  uint8_t payload_type   = ul_nas->GetPayloadContainerType();
  uint8_t pdu_session_id = 0;
  ul_nas->GetPduSessionId(pdu_session_id);

  uint8_t request_type = 0;
  if (!ul_nas->GetRequestType(request_type)) {
    Logger::amf_n1().debug("Request Type is not available");
    // TODO:
  }

  bstring sm_msg = nullptr;
  bstring did_msg = nullptr;

  if (((request_type & 0x07) == PDU_SESSION_INITIAL_REQUEST) or
      ((request_type & 0x07) == EXISTING_PDU_SESSION)) {
    // SNSSAI
    SNSSAI_t snssai = {};
    if (!ul_nas->GetSNssai(snssai)) {  // If no SNSSAI in this message, use the
                                       // one in Registration Request
      Logger::amf_n1().debug(
          "No Requested NSSAI available in UlNasTransport, use NSSAI from "
          "Requested/Configured NSSAI!");

      std::shared_ptr<nas_context> nc = {};
      if (!amf_n1_inst->amf_ue_id_2_nas_context(amf_ue_ngap_id, nc)) {
        Logger::amf_n1().warn(
            "No existed nas_context with amf_ue_ngap_id(0x%x)", amf_ue_ngap_id);
        return;
      }

      // TODO: Only use the first one for now if there's multiple requested
      // NSSAI since we don't know which slice associated with this PDU session
      if (nc->allowed_nssai.size() > 0) {
        snssai = nc->allowed_nssai[0];
        Logger::amf_n1().debug(
            "Use first Requested S-NSSAI %s", snssai.ToString().c_str());
      } else {
        // Otherwise, use first default subscribed S-NSSAI if available
        bool found = false;
        for (const auto& sn : nc->subscribed_snssai) {
          if (sn.first) {
            snssai = sn.second;
            Logger::amf_n1().debug(
                "Use Default Configured S-NSSAI %s", snssai.ToString().c_str());
            found = true;
            break;
          }
        }

        if (!found) {
          std::vector<struct SNSSAI_s> common_nssais;
          // Find UE Context
          std::shared_ptr<ue_context> uc = {};
          if (!find_ue_context(nc->ran_ue_ngap_id, nc->amf_ue_ngap_id, uc)) {
            Logger::amf_n1().warn("Cannot find the UE context");
            return;
          }
          amf_n2_inst->get_common_NSSAI(
              nc->ran_ue_ngap_id, uc->gnb_id, common_nssais);

          // Use common NSSAI between gNB and AMF
          for (auto s : common_nssais) {
            snssai.sst = s.sst;
            snssai.sd  = s.sd;
            if (s.sd == SD_NO_VALUE) {
              snssai.length = SST_LENGTH;
            } else {
              snssai.length = SST_LENGTH + SD_LENGTH;
            }
            Logger::amf_n1().debug(
                "Use common S-NSSAI (SST 0x%x, SD 0x%x)", s.sst, s.sd);
            found = true;
            break;
          }
        }

        if (!found) {
          snssai.sst    = DEFAULT_SST;
          snssai.sd     = SD_NO_VALUE;
          snssai.length = SST_LENGTH;
          Logger::amf_n1().debug(
              "Default S-NSSAI (SST 0x%x, SD 0x%x)", snssai.sst, snssai.sd);
        }
      }
    }

    Logger::amf_n1().debug(
        "S_NSSAI for this PDU Session %s", snssai.ToString().c_str());

    bstring dnn = bfromcstr(DEFAULT_DNN);

    if (!ul_nas->GetDnn(dnn)) {
      Logger::amf_n1().debug(
          "No DNN available in UlNasTransport, use default DNN: %s",
          DEFAULT_DNN);
      // TODO: use default DNN for the corresponding NSSAI
    }

    // Use DNN as case insensitive
    amf_conv::to_lower(dnn);

    output_wrapper::print_buffer(
        "amf_n1", "Decoded DNN Bit String", (uint8_t*) bdata(dnn),
        blength(dnn));

    switch (payload_type) {
      case N1_SM_INFORMATION: {
        // Get payload container
        ul_nas->GetPayloadContainer(sm_msg);
        //Get DID buffer
        ul_nas->GetPayloadContainerDID(did_msg);

        std::shared_ptr<itti_nsmf_pdusession_create_sm_context> itti_msg =
            std::make_shared<itti_nsmf_pdusession_create_sm_context>(
                TASK_AMF_N1, TASK_AMF_SBI);
        itti_msg->ran_ue_ngap_id = ran_ue_ngap_id;
        itti_msg->amf_ue_ngap_id = amf_ue_ngap_id;
        itti_msg->req_type       = request_type;
        itti_msg->pdu_sess_id    = pdu_session_id;
        itti_msg->dnn            = bstrcpy(dnn);
        itti_msg->sm_msg         = bstrcpy(sm_msg);
        itti_msg->snssai.sST     = snssai.sst;
        itti_msg->snssai.sD      = std::to_string(snssai.sd);
        itti_msg->plmn.mnc       = plmn.mnc;
        itti_msg->plmn.mcc       = plmn.mcc;

        int ret = itti_inst->send_msg(itti_msg);
        if (0 != ret) {
          Logger::amf_n1().error(
              "Could not send ITTI message %s to task TASK_AMF_SBI",
              itti_msg->get_msg_name());
        }


    // std::lock_guard<std::mutex> lock(mtx);
    // if (processed_pdu_sessions.find(pdu_session_id) == processed_pdu_sessions.end()){

        std::string did_str = bstringToString(did_msg);
        if (!did_str.empty()) {

            Logger::amf_n1().debug("raw did (bstring): %s", bstr2cstr(did_msg, '\0'));
            Logger::amf_n1().debug("converted did string; %s", did_str.c_str());

            
            std::string remoteUri = "http://172.17.0.1:8004/dper/setdid";
            // std::string remoteUri = "http://127.0.0.1:8001/dper/setdid";
            // std::string remoteUri = "http://172.17.0.1:8004/dper/setdid";


            std::string msgBody = did_str;
            nlohmann::json response;
            uint32_t response_code;
            int http_version = 1;
            
        
            amf_sbi_inst->curl_http_client_DID(
              remoteUri, "POST", msgBody.c_str(), response, response_code, http_version);

            }
            // Logger::amf_n1().debug("U-DID has been extracted for pdu_ID:[%hhu] ",pdu_session_id);
            // Logger::amf_n1().debug("U-DID has been extracted:  %s", did);

            // std::cout << "U-DID has been extracted :" << did << std::endl;

    // }
      



      } break;
      default: {
        Logger::amf_n1().debug("Transport message un supported");
      }
    }

  } else {
    switch (payload_type) {
      case N1_SM_INFORMATION: {
        // Get payload container
        ul_nas->GetPayloadContainer(sm_msg);

        std::shared_ptr<itti_nsmf_pdusession_update_sm_context> itti_msg =
            std::make_shared<itti_nsmf_pdusession_update_sm_context>(
                TASK_AMF_N1, TASK_AMF_SBI);

        itti_msg->ran_ue_ngap_id = ran_ue_ngap_id;
        itti_msg->amf_ue_ngap_id = amf_ue_ngap_id;
        itti_msg->pdu_session_id = pdu_session_id;
        itti_msg->n1sm           = bstrcpy(sm_msg);
        itti_msg->is_n1sm_set    = true;

        int ret = itti_inst->send_msg(itti_msg);
        if (0 != ret) {
          Logger::amf_n1().error(
              "Could not send ITTI message %s to task TASK_AMF_SBI",
              itti_msg->get_msg_name());
        }

      } break;
      default: {
        Logger::amf_n1().debug("Transport message is not supported");
      }
    }
  }
}
```

- component/oai-amf/src/nas/msgs/UlNasTransport.cpp
```
//------------------------------------------------------------------------------
void UlNasTransport::GetPayloadContainerDID(bstring& did_payloadcontainer) const {
  ie_payload_container.GetValueDID(did_payloadcontainer);
}
```

- component/oai-amf/src/nas/msgs/UlNasTransport.hpp
```
class UlNasTransport : public NasMmPlainHeader {
 public:
  UlNasTransport();
  ~UlNasTransport();

  void SetHeader(uint8_t security_header_type);

  int Encode(uint8_t* buf, int len);
  int Decode(uint8_t* buf, int len);

  void SetPayloadContainerType(uint8_t value);
  uint8_t GetPayloadContainerType() const;

  void SetPayloadContainer(const std::vector<PayloadContainerEntry>& content);
  void GetPayloadContainer(std::vector<PayloadContainerEntry>& content) const;
  void GetPayloadContainer(bstring& content) const;
  //DID
  void GetPayloadContainerDID(bstring& content) const;
```

- component/oai-amf/src/nas/ies/PayloadContainer.hpp:
```
class PayloadContainer : Type6NasIe {
 public:
  PayloadContainer();
  PayloadContainer(uint8_t iei);
  PayloadContainer(const bstring& b);
  PayloadContainer(uint8_t iei, const bstring& b);
  PayloadContainer(const std::vector<PayloadContainerEntry>& content);
  PayloadContainer(
      const uint8_t iei, const std::vector<PayloadContainerEntry>& content);
  ~PayloadContainer();

  static std::string GetIeName() { return kPayloadContainerIeName; }

  // void setValue(uint8_t iei, uint8_t value);
  int Encode(uint8_t* buf, int len, uint8_t type);
  int Decode(uint8_t* buf, int len, bool is_iei, uint8_t type);

  void SetValue(const bstring& cnt);
  bool GetValue(bstring& cnt) const;

  void SetValue(const std::vector<PayloadContainerEntry>& content);
  bool GetValue(std::vector<PayloadContainerEntry>& content) const;
  //DID
  bool GetValueDID(bstring& cnt) const;
   private:
  std::optional<bstring> content;
  std::optional<std::vector<PayloadContainerEntry>> CONTENT;
  std::optional<bstring> did_payloadcontainer;

};

```

- component/oai-amf/src/nas/ies/PayloadContainer.cpp
```
//DID content extract

bool PayloadContainer::GetValueDID(bstring& cnt) const {
  if (did_payloadcontainer.has_value()) {
    cnt = did_payloadcontainer.value();
    return true;
  }
  return false;
}
```
```
//------------------------------------------------------------------------------
int PayloadContainer::Decode(uint8_t* buf, int len, bool is_iei, uint8_t type) {
  Logger::nas_mm().debug("Decoding %s", GetIeName().c_str());
  int decoded_size = 0;


   for (int i=0; i < len; i++) {
    Logger::nas_mm().debug("buf1[%d] = 0x%x", i, buf[i]);
  }

  // IEI and Length
  uint16_t ie_len         = 0;
  int decoded_header_size = Type6NasIe::Decode(buf + decoded_size, len, is_iei);
  if (decoded_header_size == KEncodeDecodeError) return KEncodeDecodeError;
  decoded_size += decoded_header_size;
  ie_len = GetLengthIndicator();

  if (type != MULTIPLE_PAYLOADS) {  // not multiple payloads
    uint8_t octet       = 0;
    bstring content_tmp = {};
    content_tmp         = blk2bstr(buf + decoded_size, ie_len);
    content             = std::optional<bstring>(content_tmp);
    decoded_size += ie_len;
    
  std::cout << "decoded_size(if): " << decoded_size << std::endl;
  
  for (int i= decoded_size; i < len; i++) {
    Logger::nas_mm().debug("if buf2[%d] = 0x%x", i, buf[i]);
  }


  if (content) {
    std::cout << "Decoded content: ";
    print_bstring(content.value());

  }else{
    std::cout << "content is empty"<<std::endl;
  }

  if (content_tmp && blength(content_tmp) > 0) {
    std::cout << "Decoded content_temp: ";
    print_bstring(content_tmp);

  }else{
    std::cout << "content_tmp is empty"<<std::endl;
  }

  uint8_t* data = (uint8_t*)bdata(content.value());
  int len = blength(content.value());  

  //DID content extraction
  int index = -1;
  for (int i = 0; i < len; i++) {
    if (data[i] == 0x44) {
      index = i;
      break;
    }
  }

  if (index != -1) {
    Logger::nas_mm().debug( "Found 0x44 at index: %d ",index);

    if (index  <= len){
      did_payloadcontainer = blk2bstr(data + index , len);
      Logger::nas_mm().debug( "Extracted did byte encoded data: ");
      print_bstring(did_payloadcontainer.value());

      //release the DID content in payloadcontainer
      bstring new_content = blk2bstr(data, index - 1);

      if (content.has_value()){
        bdestroy(content.value());
      }

      content = std::optional<bstring>(new_content);

      Logger::nas_mm().debug("Remaining content after removing DID:");
      print_bstring(content.value());


    }else {
      Logger::nas_mm().debug( "Not enough data after 0x44 to extract 9+64 bits. ");
    }
  }else{
    Logger::nas_mm().debug( "0x44 not found in content. ");
  }

    
    
    
    return decoded_size;
  }
```

- component/oai-smf/etc/config_fromhub.yaml 添加了一个新的config，这是从dockerhub自动生成的config中拉下来再更新DNN的
```
################################################################################
# Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The OpenAirInterface Software Alliance licenses this file to You under
# the OAI Public License, Version 1.1  (the "License"); you may not use this file
# except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.openairinterface.org/?page_id=698
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------------
# For more information about the OpenAirInterface (OAI) Software Alliance:
#      contact@openairinterface.org
################################################################################

# OAI CN Configuration File
### This file can be used by all OAI NFs
### Some fields are specific to an NF and will be ignored by other NFs

## NOTE ON YAML ANCHORS ##
# We use YAML anchors to ease the configuration and to avoid duplicating parts of the configuration.
# This is especially true for the SNSSAIs, as we have to define them for multiple NFs.
# Please note that the use of anchors is not mandatory, and you can define the SNSSAI in each NF yourself.
# You can read more about anchors here: https://yaml.org/spec/1.2.2/#anchors-and-aliases

############# Common configuration

# Log level for all the NFs
log_level:
  general: debug

# If you enable registration, the other NFs will use the NRF discovery mechanism
register_nf:
  general: yes

http_version: 2

############## SBI Interfaces
### Each NF takes its local SBI interfaces and remote interfaces from here, unless it gets them using NRF discovery mechanisms
nfs:
  amf:
    host: oai-amf
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0
    n2:
      interface_name: eth0
      port: 38412
  smf:
    host: oai-smf
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0
    n4:
      interface_name: eth0
      port: 8805
  udm:
    host: oai-udm
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0
  udr:
    host: oai-udr
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0
  ausf:
    host: oai-ausf
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0
  nrf:
    host: oai-nrf
    sbi:
      port: 8080
      api_version: v1
      interface_name: eth0

#### Common for UDR and AMF
database:
  host: mysql
  user: test
  type: mysql
  password: test
  database_name: oai_db
  generate_random: true
  connection_timeout: 300 # seconds

## general single_nssai configuration
## Defines YAML anchors, which are reused in the config file
snssais:
  - &embb_slice1
    sst: 1
  - &embb_slice2
    sst: 1
    sd: 000001 # in hex
  - &custom_slice
    sst: 222
    sd: 00007B # in hex

############## NF-specific configuration
amf:
  amf_name: "OAI-AMF"
  # This really depends on if we want to keep the "mini" version or not
  support_features_options:
    enable_simple_scenario: no # "no" by default with the normal deployment scenarios with AMF/SMF/UPF/AUSF/UDM/UDR/NRF.
                               # set it to "yes" to use with the minimalist deployment scenario (including only AMF/SMF/UPF) by using the internal AUSF/UDM implemented inside AMF.
                               # There's no NRF in this scenario, SMF info is taken from "nfs" section.
    enable_nssf: no
    enable_smf_selection: yes
  relative_capacity: 30
  statistics_timer_interval: 20  # in seconds
  emergency_support: false
  served_guami_list:
    - mcc: 208
      mnc: 95
      amf_region_id: 01
      amf_set_id: 001
      amf_pointer: 01
    - mcc: 001
      mnc: 01
      amf_region_id: 01
      amf_set_id: 001
      amf_pointer: 01
  plmn_support_list:
    - mcc: 208
      mnc: 95
      tac: 0xa000
      nssai:
        - *embb_slice1
        - *embb_slice2
        - *custom_slice
  supported_integrity_algorithms:
    # - "NIA0"
    - "NIA1"
    - "NIA2"
  supported_encryption_algorithms:
    # - "NEA0"
    - "NEA1"
    - "NEA2"

smf:
  ue_mtu: 1500
  support_features:
    use_local_subscription_info: yes # Use infos from local_subscription_info or from UDM
    use_local_pcc_rules: yes # Use infos from local_pcc_rules or from PCF
  # we resolve from NRF, this is just to configure usage_reporting
  # TODO SMF does not support this yet to use this value per UPF. If we implement this, we can remove this file and use basic_nrf_config
  upfs:
    - host: vpp-upf.node.5gcn.mnc95.mcc208.3gppnetwork.org
      config:
        enable_usage_reporting: yes
  ue_dns:
    primary_ipv4: "172.21.3.100"
    primary_ipv6: "2001:4860:4860::8888"
    secondary_ipv4: "8.8.8.8"
    secondary_ipv6: "2001:4860:4860::8888"
  ims:
    pcscf_ipv4: "127.0.0.1"
    pcscf_ipv6: "fe80::7915:f408:1787:db8b"
  # the DNN you configure here should be configured in "dnns"
  # follows the SmfInfo datatype from 3GPP TS 29.510
  smf_info:
    sNssaiSmfInfoList:
      - sNssai: *embb_slice1
        dnnSmfInfoList:
          - dnn: "oai"
      - sNssai: *embb_slice2
        dnnSmfInfoList:
          - dnn: "oai.ipv4"
      - sNssai: *custom_slice
        dnnSmfInfoList:
          - dnn: "default"
  local_subscription_infos:
    - single_nssai: *embb_slice1
      dnn: "oai"
      qos_profile:
        5qi: 9
        session_ambr_ul: "200Mbps"
        session_ambr_dl: "400Mbps"
    - single_nssai: *embb_slice2
      dnn: "oai.ipv4"
      qos_profile:
        5qi: 9
        session_ambr_ul: "100Mbps"
        session_ambr_dl: "200Mbps"
    - single_nssai: *custom_slice
      dnn: "default"
      qos_profile:
        5qi: 9
        session_ambr_ul: "50Mbps"
        session_ambr_dl: "100Mbps"

## DNN configuration
dnns:
  - dnn: "oai"
    pdu_session_type: "IPV4"
    ipv4_subnet: "12.1.1.192/26"
  - dnn: "oai.ipv4"
    pdu_session_type: "IPV4"
    ipv4_pool: "12.1.1.128/26"
  - dnn: "default"
    pdu_session_type: "IPV4"
    ipv4_pool: "12.1.1.0/25"
  - dnn: "ims"
    pdu_session_type: "IPV4V6"
    ipv4_pool: "14.1.1.0/24"
  # - dnn: "oai"
  #   pdu_session_type: "IPV4"
  #   ipv4_subnet: "12.1.1.128/25"
  # - dnn: "oai.ipv4"
  #   pdu_session_type: "IPV4"
  #   ipv4_subnet: "12.1.1.64/26"
  # - dnn: "default"
  #   pdu_session_type: "IPV4"
  #   ipv4_subnet: "12.1.1.0/26"
  # - dnn: "ims"
  #   pdu_session_type: "IPV4V6"
  #   ipv4_subnet: "14.1.1.2/24"

```


- src/gnb/rrc/sap.cpp:

```
#include <sys/time.h>
#include <time.h>
#include "log_time.h"

namespace nr::gnb
{

void GnbRrcTask::handleRlsSapMessage(NmGnbRlsToRrc &msg)
{
    switch (msg.present)
    {
    case NmGnbRlsToRrc::SIGNAL_DETECTED: {
        m_logger->debug("UE[%d] new signal detected", msg.ueId);
        triggerSysInfoBroadcast();
        
            // 获取带微秒的当前时间
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
            now.time_since_epoch()
        ) % 1000000;
        // 转换成本地时间格式
        std::tm tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
        
        // 格式化时间字符串
        char buffer[80];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        
        // 追加写入文件
        std::ofstream file("timelogs.txt", std::ios::app);
        if (file) {
            file << "UE启动的时间: " << buffer << "." 
                << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
        }
```

## dnn改造思路 25-03-06
- component/oai-smf/src/smf_app/smf_config.cpp
```

void smf_config::to_smf_config() {
  log_level    = spdlog::level::from_str(config::log_level());
  auto smf_cfg = smf();

  use_local_subscription_info =
      smf_cfg->get_smf_support_features().use_local_subscription_info();
  use_local_pcc_rules =
      smf_cfg->get_smf_support_features().use_local_pcc_rules();

  // TODO discover PCF is not implemented
  discover_pcf = false;

  local_interface _n4 = smf()->get_n4();

  n4.port    = _n4.get_port();
  n4.addr4   = _n4.get_addr4();
  n4.addr6   = _n4.get_addr6();
  n4.if_name = _n4.get_if_name();
  n4.mtu     = _n4.get_mtu();

  // TODO these values are not configurable anymore
  sbi.thread_rd_sched_params.sched_priority   = 90;
  itti.itti_timer_sched_params.sched_priority = 85;
  itti.n4_sched_params.sched_priority         = 84;
  itti.smf_app_sched_params.sched_priority    = 84;
  itti.async_cmd_sched_params.sched_priority  = 84;
  n4.thread_rd_sched_params.sched_priority    = 90;

  force_push_pco = true;

  sbi.port        = smf_cfg->get_sbi().get_port();
  sbi.addr4       = smf_cfg->get_sbi().get_addr4();
  sbi.addr6       = smf_cfg->get_sbi().get_addr6();
  sbi.if_name     = smf_cfg->get_sbi().get_if_name();
  sbi_http2_port  = smf_cfg->get_sbi().get_port();
  sbi_api_version = smf_cfg->get_sbi().get_api_version();
  http_version    = get_http_version();

  // DNNs
  for (const auto& cfg_dnn : get_dnns()) {
    dnn_t dnn;
    dnn.pdu_session_type  = cfg_dnn.get_pdu_session_type();
    dnn.dnn               = cfg_dnn.get_dnn();
    dnn.ue_pool_range_low = cfg_dnn.get_ipv4_pool_start();
    // we need to add one IP as it is reserved for the GW
    dnn.ue_pool_range_low.s_addr += be32toh(1);
    dnn.ue_pool_range_high = cfg_dnn.get_ipv4_pool_end();

    logger::logger_registry::get_logger(LOGGER_NAME)
        .debug(
            "DNN %s: -- First UE IPv4: %s -- Last UE IPv4: %s", dnn.dnn,
            conv::toString(dnn.ue_pool_range_low),
            conv::toString(dnn.ue_pool_range_high));

    dnn.paa_pool6_prefix     = cfg_dnn.get_ipv6_prefix();
    dnn.paa_pool6_prefix_len = cfg_dnn.get_ipv6_prefix_length();
    dnns[dnn.dnn]            = dnn;
  }
}
```

- 其中`dnn.ue_pool_range_low = cfg_dnn.get_ipv4_pool_start();`和`dnn.ue_pool_range_high = cfg_dnn.get_ipv4_pool_end();`很可疑；


- component/oai-smf/src/oai-cn5g-common-src/config/config_types.cpp
```
[[nodiscard]] const in_addr& dnn_config::get_ipv4_pool_start() const {
  return m_ipv4_pool_start_ip;
}

[[nodiscard]] const in_addr& dnn_config::get_ipv4_pool_end() const {
  return m_ipv4_pool_end_ip;
}
```

- component/oai-smf/src/oai-cn5g-common-src/config/config_types.hpp
```
class dnn_config : public config_type {
 private:
  string_config_value m_dnn;
  string_config_value m_pdu_session_type;
  string_config_value m_ipv4_subnet;
  string_config_value m_ipv6_prefix;
  ue_dns m_ue_dns;

  // generated
  int m_ipv4_prefix{};
  in_addr m_ipv4_subnet_ip{};

  in_addr m_ipv4_pool_start_ip{};
  in_addr m_ipv4_pool_end_ip{};
  in6_addr m_ipv6_prefix_ip{};

 private:
  uint8_t m_ipv6_prefix_length{};
  pdu_session_type_t m_pdu_session_type_generated;

 public:
  explicit dnn_config(
      const std::string& dnn, const std::string& pdu_type,
      const std::string& ipv4_subnet, const std::string& ipv6_prefix);

  void from_yaml(const YAML::Node& node) override;
  nlohmann::json to_json() override;
  bool from_json(const nlohmann::json& json_data) override;

  [[nodiscard]] std::string to_string(const std::string& indent) const override;

  void validate() override;

  [[nodiscard]] const in_addr& get_ipv4_pool_start() const;
  [[nodiscard]] const in_addr& get_ipv4_pool_end() const;
  [[nodiscard]] const in_addr& get_ipv4_subnet() const;
  [[nodiscard]] const in_addr& get_ipv4_subnet_mask() const;
  [[nodiscard]] const int& get_ipv4_subnet_prefix() const;
  [[nodiscard]] const in6_addr& get_ipv6_prefix() const;
  [[nodiscard]] uint8_t get_ipv6_prefix_length() const;
  [[nodiscard]] const pdu_session_type_t& get_pdu_session_type() const;
  [[nodiscard]] const std::string& get_dnn() const;
  [[nodiscard]] const ue_dns& get_ue_dns() const;
  void set_ue_dns(const ue_dns& dns);
};
```

- `m_ipv4_pool_start_ip{};`在这没有赋值，说明他应该是`in_addr`提供了

- 同一个文件：
```
struct in_addr
  {
    in_addr_t s_addr;
  };

```



[2025-03-06 10:35:29.859] [config ] [info] DNNs:
[2025-03-06 10:35:29.859] [config ] [info] - DNN:
[2025-03-06 10:35:29.859] [config ] [info]     + DNN......................................: oai
[2025-03-06 10:35:29.859] [config ] [info]     + PDU session type.........................: IPV4
[2025-03-06 10:35:29.859] [config ] [info]     + IPv4 subnet..............................: 12.1.1.192/26
[2025-03-06 10:35:29.859] [config ] [info]     + DNS Settings:
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv4.......................: 172.21.3.100
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv6.......................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv4.....................: 8.8.8.8
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv6.....................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info] - DNN:
[2025-03-06 10:35:29.859] [config ] [info]     + DNN......................................: oai.ipv4
[2025-03-06 10:35:29.859] [config ] [info]     + PDU session type.........................: IPV4
[2025-03-06 10:35:29.859] [config ] [info]     + IPv4 subnet..............................: 12.1.1.0/24
[2025-03-06 10:35:29.859] [config ] [info]     + DNS Settings:
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv4.......................: 172.21.3.100
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv6.......................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv4.....................: 8.8.8.8
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv6.....................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info] - DNN:
[2025-03-06 10:35:29.859] [config ] [info]     + DNN......................................: default
[2025-03-06 10:35:29.859] [config ] [info]     + PDU session type.........................: IPV4
[2025-03-06 10:35:29.859] [config ] [info]     + IPv4 subnet..............................: 12.1.1.0/24
[2025-03-06 10:35:29.859] [config ] [info]     + DNS Settings:
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv4.......................: 172.21.3.100
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv6.......................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv4.....................: 8.8.8.8
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv6.....................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info] - DNN:
[2025-03-06 10:35:29.859] [config ] [info]     + DNN......................................: ims
[2025-03-06 10:35:29.859] [config ] [info]     + PDU session type.........................: IPV4V6
[2025-03-06 10:35:29.859] [config ] [info]     + IPv6 prefix..............................: 
[2025-03-06 10:35:29.859] [config ] [info]     + IPv4 subnet..............................: 12.1.1.0/24
[2025-03-06 10:35:29.859] [config ] [info]     + DNS Settings:
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv4.......................: 172.21.3.100
[2025-03-06 10:35:29.859] [config ] [info]       - primary_dns_ipv6.......................: 2001:4860:4860::8888
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv4.....................: 8.8.8.8
[2025-03-06 10:35:29.859] [config ] [info]       - secondary_dns_ipv6.....................: 2001:4860:4860::8888

不知道为什么，他不按照我写的config.yaml来，读了一些乱七八糟的出来

而且，smf和amf互相能ping通，但是我启动ue，amf会显示值哦阿不到smf