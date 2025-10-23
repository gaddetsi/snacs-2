raph data written to twitter-graph.csv
Total unique edges: 149367
Number of edges: 149367
Number of nodes: 85384
Number of strongly connected components: 79993
Size of largest strongly connected component: 4859
Number of weakly connected components: 2789
Size of largest weakly connected component: 75310
Density of the graph: 2.048833902783156e-05
Average clustering coefficient: 0.0671869596917758
Giant component - Number of nodes: 75310, Number of edges: 138911
Average distance in the giant component: 6.295430261585447
Top 20 nodes by Degree Centrality:
tamaraschilling    0.009866
mashable           0.006666
medic_ray          0.005285
americandream09    0.005205
drjennifer         0.005152
elocio             0.004966
erenwall           0.004833
nachhi             0.004634
bacieabbracci      0.004488
teddy_salad        0.004316
centerpet          0.004156
lauralassiter      0.004130
pcpitcrew          0.003745
jhillstephens      0.003691
straightstreet     0.003665
kellythomas1       0.003625
secularstupid      0.003559
bobgarrett         0.003439
doc_remy           0.003333
ohmichael          0.003333
Name: Degree Centrality, dtype: float64

Top 20 nodes by Betweenness Centrality:
tamaraschilling    0.007358
americandream09    0.004456
straightstreet     0.002849
medic_ray          0.002539
centerpet          0.002242
nachhi             0.002182
teddy_salad        0.002167
drjennifer         0.002153
elocio             0.002061
bobcallahan        0.002031
modelsupplies      0.001911
doc_remy           0.001859
bacieabbracci      0.001852
josephranseth      0.001819
lauralassiter      0.001794
jhillstephens      0.001731
sharonhayes        0.001574
java4two           0.001454
dpbkmb             0.001419
ciaobella50        0.001416
Name: Betweenness Centrality, dtype: float64

Top 20 nodes by Closeness Centrality:
mashable           0.028660
matt_369           0.027572
starlingpoet       0.027214
holdemtalkradio    0.026598
bonniestwit        0.026523
tamaraschilling    0.026265
thelifehackpost    0.026050
americandream09    0.025988
lorimoreno         0.025912
centerpet          0.025835
faithgoddess7      0.025688
modelsupplies      0.025688
americanwomannn    0.025644
billzucker         0.025573
jason_pollock      0.025564
emarketingguru     0.025509
weizenbaum         0.025473
tap29              0.025433
sharonhayes        0.025428
nurul54            0.025394
Name: Closeness Centrality, dtype: float64

Rank correlation between Degree and Betweenness Centrality: 0.56933847779787
Rank correlation between Degree and Closeness Centrality: 0.22697552957132558
Rank correlation between Betweenness and Closeness Centrality: 0.2425306144387351


[i] Found 698 communities in giant component (undirected).
  Community 1: size=17491  (sample members: ['tolemac', 'melaniemayron56', 'sherrybutlerpr', 'sfinleynh', 'mountainkat2', 'carenews', 'fluffydbunny', 'debbiejjohnson', 'tweetlater', 'restrictor'])
  Community 2: size=6202  (sample members: ['mywherehaus', 'anglia_execs', 'little_lin', 'atmospeer', 'goldenhillcows', 'macdog73', 'sapper6', 'mindjet', 'cl0wnzee', 'drummergrl'])
  Community 3: size=4977  (sample members: ['_mom24', 'candice202', 'camodadogg', 'nnus', 'ecosandy', 'grahamfarrar', 'farmafrica', 'simpliflying', 'threebysea', 'nealfrankle'])
  Community 4: size=3274  (sample members: ['glueazy', 'etanowitz', 'slimmduddy', 'charissarobins', 'deltaladytoday', 'insidehoops', 'kpdolla', 'coolnerdgav', 'reallamarodom', 'mistyhofstetter'])
  Community 5: size=2803  (sample members: ['kellycairns', 'imageisfound', 'aqhhof', 'flowersbyfarha', 'cullenhelen', 'jrwadsworth18', 'tnpd', 'tweeterism', 'photonconcepts', 'jcverdie'])

  i] Parsed twitter-small.tsv -> twitter_graph.csv
[i] Total unique edges (before threshold): 149367
[i] Unique edges written (w >= 1): 149367
[i] Unique nodes encountered: 85384
[i] Nodes: 85384  Edges: 149367  Density: 0.000020
[i] Strongly connected components: 79993  (largest sizes: [4859, 9, 6, 6, 5])
[i] Weakly connected components: 2789  (largest sizes: [75310, 22, 21, 21, 20])
[i] Average clustering coefficient (undirected): 0.067187
[i] Giant component nodes: 75310, edges: 138911
[i] Connected sample nodes: 200, edges: 503
[i] Approximated average distance (sample_size=200): 1.9747
[i] Saved degree scatter (log-log) to degree_scatter_twitter-small.png
[i] Saved distance distribution plot to distance_dist_twitter-small.png
[i] Saved weight distribution (log-log) to weight_dist_twitter-small.png
[i] Top nodes by in-degree (count):
mashable           502
matt_369           234
tweetmeme          223
starlingpoet       221
holdemtalkradio    195
bonniestwit        172
emarketingguru     149
tamaraschilling    149
centerpet          144
thelifehackpost    131
sharonhayes        129
elocio             126
jonnerz            124
jason_pollock      119
americanwomannn    117
peterfacinelli     113
fridayluv          112
faithgoddess7      108
straightstreet     107
lorimoreno         105
Name: in_degree, dtype: int64

[i] Top nodes by out-degree (count):
tamaraschilling    594
erenwall           332
drjennifer         327
medic_ray          311
nachhi             296
americandream09    288
bacieabbracci      279
teddy_salad        278
pcpitcrew          259
elocio             248
lauralassiter      244
kellythomas1       243
secularstupid      233
bobgarrett         227
carelea            222
june_prissydog     214
indyenigma         211
jhillstephens      209
imbeeyo            199
doc_remy           196
Name: out_degree, dtype: int64

[i] Top nodes by degree centrality (normalized):
tamaraschilling    0.009866
mashable           0.006666
medic_ray          0.005285
americandream09    0.005205
drjennifer         0.005152
elocio             0.004966
erenwall           0.004833
nachhi             0.004634
bacieabbracci      0.004488
teddy_salad        0.004316
centerpet          0.004156
lauralassiter      0.004130
pcpitcrew          0.003745
jhillstephens      0.003691
straightstreet     0.003665
kellythomas1       0.003625
secularstupid      0.003559
bobgarrett         0.003439
doc_remy           0.003333
ohmichael          0.003333
Name: deg_centrality, dtype: float64

[i] Top nodes by betweenness:
josephranseth      0.005838
sharonhayes        0.005754
americandream09    0.003875
tamaraschilling    0.003616
straightstreet     0.003579
johnfmoore         0.003185
planethealer       0.003135
txponygirl         0.003106
ginaatl            0.002951
fashiongrail       0.002917
imikepayne         0.002903
franciscojsaez     0.002895
franktrigg         0.002889
qwilite            0.002880
harleywonderpug    0.002878
grownfolksmusic    0.002875
taywhit            0.002874
joannematthews     0.002764
demonfactory       0.002714
kristalashely      0.002694
Name: betweenness, dtype: float64

[i] Top nodes by closeness:
mashable           0.028660
matt_369           0.027572
starlingpoet       0.027214
holdemtalkradio    0.026598
bonniestwit        0.026523
tamaraschilling    0.026265
thelifehackpost    0.026050
americandream09    0.025988
lorimoreno         0.025912
centerpet          0.025835
faithgoddess7      0.025688
modelsupplies      0.025688
americanwomannn    0.025644
billzucker         0.025573
jason_pollock      0.025564
emarketingguru     0.025509
weizenbaum         0.025473
tap29              0.025433
sharonhayes        0.025428
nurul54            0.025394
Name: closeness, dtype: float64

Spearman correlations (deg vs bet, deg vs close, bet vs close):
deg vs bet: 0.502
deg vs close: 0.227
bet vs close: 0.322
[i] Found 698 communities in giant component (undirected).
  Community 1: size=17491  (sample members: ['tolemac', 'melaniemayron56', 'sherrybutlerpr', 'sfinleynh', 'mountainkat2', 'carenews', 'fluffydbunny', 'debbiejjohnson', 'tweetlater', 'restrictor'])
  Community 2: size=6202  (sample members: ['mywherehaus', 'anglia_execs', 'little_lin', 'atmospeer', 'goldenhillcows', 'macdog73', 'sapper6', 'mindjet', 'cl0wnzee', 'drummergrl'])
  Community 3: size=4977  (sample members: ['_mom24', 'candice202', 'camodadogg', 'nnus', 'ecosandy', 'grahamfarrar', 'farmafrica', 'simpliflying', 'threebysea', 'nealfrankle'])
  Community 4: size=3274  (sample members: ['glueazy', 'etanowitz', 'slimmduddy', 'charissarobins', 'deltaladytoday', 'insidehoops', 'kpdolla', 'coolnerdgav', 'reallamarodom', 'mistyhofstetter'])
  Community 5: size=2803  (sample members: ['kellycairns', 'imageisfound', 'aqhhof', 'flowersbyfarha', 'cullenhelen', 'jrwadsworth18', 'tnpd', 'tweeterism', 'photonconcepts', 'jcverdie'])

  [i] Parsed twitter-larger.tsv -> twitter_graph_larger.csv
[i] Total unique edges (before threshold): 1275114
[i] Unique edges written (w >= 1): 1275114
[i] Unique nodes encountered: 471077
[i] Nodes: 471077  Edges: 1275114  Density: 0.000006
[i] Strongly connected components: 413269  (largest sizes: [54895, 15, 9, 7, 7])
[i] Weakly connected components: 10077  (largest sizes: [441346, 50, 29, 26, 24])
[i] Average clustering coefficient (undirected): 0.100980
[i] Giant component nodes: 441346, edges: 1203210
[i] Connected sample nodes: 200, edges: 805
[i] Approximated average distance (sample_size=200): 1.9595
[i] Saved degree scatter (log-log) to degree_scatter_twitter-larger.png
[i] Saved distance distribution plot to distance_dist_twitter-larger.png
[i] Saved weight distribution (log-log) to weight_dist_twitter-larger.png
