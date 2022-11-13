#Written by Nathan A-M =^)
#Buffer-based implementation using 
#A Buffer-based approach as a reference 
import math

from studentcodeExample import bufferbased

bitrate = 0 #used to save previous bitrate

def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate ):
    #student can do whatever they want from here going forward
    global bitrate
    rate_prev=bitrate
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True)
    R_max = max(i[1] for i in R_i)
    R_min = min(i[1] for i in R_i)
    gamma = 2.5
    t = min(Video_Time, Chunk['time'] * (Chunk['left'] + int(Chunk['current'])) - Video_Time)
    t_prime = max(t / 2., 3 * Chunk['time'])
    
    if bitrate == 0:
        bitrate = R_i[-1][0]
    for i in R_i:
        if bitrate == i[0]:
            vm = math.log(i[1]/R_min)

    Q_max = 60
    Q_max_dynamic = min(Q_max, t_prime / Chunk['time'])

    V_dynamic = (Q_max_dynamic - 1) / (vm + gamma * Chunk['time'])

    argmax = -100
    for i in R_i:
        vm = math.log(i[1]/R_min)
        Q_time = Buffer_Occupancy['time']
        prev_argmax = argmax
        argmax = (V_dynamic * vm + V_dynamic * gamma * Chunk['time'] - Q_time) / i[1]
        if argmax > prev_argmax:
            result = i
    bitrate = result[0]

# '''到这里是6line'''
    if int(rate_prev) < int(bitrate):
        r = Measured_Bandwidth
        m_prime = '0'
        for i in R_i:
            if (i[1] / Chunk['time']) <= max(r, R_i[-1][1] / Chunk['time']):
                m_prime = i[0]
                break
        if int(m_prime) >= int(bitrate):
            bitrate = m_prime
        elif int(m_prime) < int(rate_prev):
            bitrate = rate_prev
        else:
            m_prime = R_i[0][0]
        bitrate = m_prime
    print(Buffer_Occupancy)
    print(bitrate)
    print(Q_max)
    return bitrate

