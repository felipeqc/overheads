set terminal postscript eps size 3.5,2.62 enhanced color
set encoding utf8

set mytics 4

set xrange [1:45]
set xtics (1, 5, 10, 15, 20, 25, 30, 35, 40, 45)

set output "SCHED.eps"
set xlabel "Número de tarefas por partição"
set ylabel "Overhead de Scheduling ({/Symbol m}s)"
set yrange [0.5:2]
set ytics (0.5,0.75,1.0,1.25,1.5,1.75,2.0)
#plot "../model/model_scheduler=EDF-WM_overhead=SCHED" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=SCHED" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=SCHED" using 3:($6*1000) title "HIME" with linespoints

set output "SCHED2.eps"
set ylabel "Overhead de Scheduling2 ({/Symbol m}s)"
set yrange [0:0.75]
set ytics (0.25,0.5,0.75)
#plot "../model/model_scheduler=EDF-WM_overhead=SCHED2" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=SCHED2" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=SCHED2" using 3:($6*1000) title "HIME" with linespoints

set output "RELEASE.eps"
set ylabel "Overhead de Release ({/Symbol m}s)"
set yrange [0.25:1.0]
set ytics (0.25,0.5,0.75,1.0)
#plot "../model/model_scheduler=EDF-WM_overhead=RELEASE" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=RELEASE" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=RELEASE" using 3:($6*1000) title "HIME" with linespoints

set output "CXS.eps"
set ylabel "Overhead de Context-switching ({/Symbol m}s)"
set yrange [0.5:1.25]
set ytics (0.5,0.75, 1.0, 1.25)
#plot "../model/model_scheduler=EDF-WM_overhead=CXS" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=CXS" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=CXS" using 3:($6*1000) title "HIME" with linespoints

set output "TICK.eps"
set ylabel "Overhead de Tick ({/Symbol m}s)"
set yrange [0:0.5]
set ytics (0.25,0.5)
#plot "../model/model_scheduler=EDF-WM_overhead=TICK" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=TICK" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=TICK" using 3:($6*1000) title "HIME" with linespoints

set output "SEND_RESCHED.eps"
set ylabel "Overhead de IPI ({/Symbol m}s)"
set yrange [0.5:1.25]
set ytics (0.5,0.75,1.0,1.25)
#plot "../model/model_scheduler=EDF-WM_overhead=SEND_RESCHED" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=SEND_RESCHED" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=SEND_RESCHED" using 3:($6*1000) title "HIME" with linespoints

set output "RELEASE_LATENCY.eps"
set ylabel "Latência das Interrupções ({/Symbol m}s)"
set yrange [0:0.25]
set ytics (0.125, 0.25)
#plot "../model/model_scheduler=EDF-WM_overhead=RELEASE_LATENCY" using 3:($6*1000) title "EDF-WM" with linespoints, \
#     "../model/model_scheduler=HIME_overhead=RELEASE_LATENCY" using 3:($6*1000) title "HIME" with linespoints
plot "../model/model_scheduler=HIME_overhead=RELEASE_LATENCY" using 3:($6*1000) title "HIME" with linespoints

#set output "PULL_TIMER.eps"
#set ylabel "Overhead do Timer de Migração ({/Symbol m}s)"
#plot "../model/model_scheduler=EDF-WM_overhead=PULL_TIMER" using 3:($6*1000) title "EDF-WM" with linespoints
