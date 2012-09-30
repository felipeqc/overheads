set terminal postscript eps size 6.0,4.0 enhanced color
set encoding utf8

set mytics 4

set xrange [1:45]
set xtics (1, 5, 10, 15, 20, 25, 30, 35, 40, 45)

set output "HIME.eps"
set xlabel "Número de tarefas por partição"
set ylabel "Overhead ({/Symbol m}s)"
set yrange [0:2]
set ytics (0.25, 0.5, 0.75,1.0,1.25,1.5,1.75,2.0)

plot "../model/model_scheduler=HIME_overhead=SCHED" using 3:($6*1000) title "Scheduling" with linespoints pt 4 lc 1 lw 4, \
     "../model/model_scheduler=HIME_overhead=SCHED2" using 3:($6*1000) title "Scheduling 2" with linespoints pt 6 lc 1 lw 4, \
     "../model/model_scheduler=HIME_overhead=RELEASE" using 3:($6*1000) title "Release" with linespoints pt 8 lw 4, \
     "../model/model_scheduler=HIME_overhead=CXS" using 3:($6*1000) title "Context-Switching" with linespoints pt 10 lw 4, \
     "../model/model_scheduler=HIME_overhead=TICK" using 3:($6*1000) title "Tick" with linespoints pt 8 lc 2 lw 4, \
     "../model/model_scheduler=HIME_overhead=SEND_RESCHED" using 3:($6*1000) title "IPI" with linespoints pt 1 lc 9  lw 4, \
     "../model/model_scheduler=HIME_overhead=RELEASE_LATENCY" using 3:($6*1000) title "Lat. de Release" with linespoints pt 7 lc 7 lw 4
