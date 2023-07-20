def lebaron(cut):
    i = cut[0]
    j = cut[1]
    k = cut[2]
    el = cut[3]
    correction = None
    if k == 1 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.173
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.104
            elif j == 3:
                correction = 1.115
            elif j == 4:
                correction = 1.163
        elif i == 3:
            if j == 1:
                correction = 1.069
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.119
            elif j == 4:
                correction = 1.140
        elif i == 4:
            if j == 1:
                correction = 1.047
            elif j == 2:
                correction = 1.063
            elif j == 3:
                correction = 1.074
            elif j == 4:
                correction = 1.030
    elif k == 2 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.248
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.184
        elif i == 3:
            if j == 1:
                correction = 1.161
            elif j == 2:
                correction = 1.161
            elif j == 3:
                correction = 1.147
            elif j == 4:
                correction = 1.168
        elif i == 4:
            if j == 1:
                correction = 1.076
            elif j == 2:
                correction = 1.078
            elif j == 3:
                correction = 1.104
            elif j == 4:
                correction = 1.146
    elif k == 3 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.187
            elif j == 2:
                correction = 1.167
            elif j == 3:
                correction = 1.139
            elif j == 4:
                correction = 1.191
    elif k == 4 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.181
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 0.990
            elif j == 4:
                correction = 1.104
        elif i == 3:
            if j == 1:
                correction = 1.015
            elif j == 2:
                correction = 1.016
            elif j == 3:
                correction = 0.946
            elif j == 4:
                correction = 1.027
        elif i == 4:
            if j == 1:
                correction = 0.925
            elif j == 2:
                correction = 0.967
            elif j == 3:
                correction = 0.977
            elif j == 4:
                correction = 1.150
    elif k == 1 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.176
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.095
            elif j == 3:
                correction = 1.130
            elif j == 4:
                correction = 1.162
        elif i == 3:
            if j == 1:
                correction = 1.073
            elif j == 2:
                correction = 1.089
            elif j == 3:
                correction = 1.115
            elif j == 4:
                correction = 1.142
        elif i == 4:
            if j == 1:
                correction = 1.058
            elif j == 2:
                correction = 1.076
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.211
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.186
            elif j == 4:
                correction = 1.194
        elif i == 3:
            if j == 1:
                correction = 1.086
            elif j == 2:
                correction = 1.130
            elif j == 3:
                correction = 1.168
            elif j == 4:
                correction = 1.177
        elif i == 4:
            if j == 1:
                correction = 1.074
            elif j == 2:
                correction = 1.102
            elif j == 3:
                correction = 1.118
            elif j == 4:
                correction = 1.174
    elif k == 3 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.237
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.203
            elif j == 4:
                correction = 1.212
        elif i == 3:
            if j == 1:
                correction = 1.080
            elif j == 2:
                correction = 1.195
            elif j == 3:
                correction = 1.211
            elif j == 4:
                correction = 1.185
        elif i == 4:
            if j == 1:
                correction = 1.140
            elif j == 2:
                correction = 1.098
            elif j == 3:
                correction = 1.191
            elif j == 4:
                correction = 1.181
    elif k == 4 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.217
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.120
            elif j == 4:
                correction = 1.180
        elif i == 3:
            if j == 1:
                correction = 1.182
            elif j == 2:
                correction = 1.115
            elif j == 3:
                correction = 1.081
            elif j == 4:
                correction = 1.111
        elif i == 4:
            if j == 1:
                correction = 1.057
            elif j == 2:
                correction = 1.119
            elif j == 3:
                correction = 1.133
            elif j == 4:
                correction = 1.033
    elif k == 1 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.182
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.128
            elif j == 4:
                correction = 1.159
        elif i == 3:
            if j == 1:
                correction = 1.076
            elif j == 2:
                correction = 1.088
            elif j == 3:
                correction = 1.131
            elif j == 4:
                correction = 1.129
        elif i == 4:
            if j == 1:
                correction = 1.060
            elif j == 2:
                correction = 1.085
            elif j == 3:
                correction = 1.103
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.221
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.171
            elif j == 3:
                correction = 1.180
            elif j == 4:
                correction = 1.213
        elif i == 3:
            if j == 1:
                correction = 1.135
            elif j == 2:
                correction = 1.148
            elif j == 3:
                correction = 1.176
            elif j == 4:
                correction = 1.197
        elif i == 4:
            if j == 1:
                correction = 1.092
            elif j == 2:
                correction = 1.119
            elif j == 3:
                correction = 1.143
            elif j == 4:
                correction = 1.182
    elif k == 3 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.238
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.160
            elif j == 3:
                correction = 1.207
            elif j == 4:
                correction = 1.230
        elif i == 3:
            if j == 1:
                correction = 1.169
            elif j == 2:
                correction = 1.191
            elif j == 3:
                correction = 1.193
            elif j == 4:
                correction = 1.210
        elif i == 4:
            if j == 1:
                correction = 1.150
            elif j == 2:
                correction = 1.133
            elif j == 3:
                correction = 1.180
            elif j == 4:
                correction = 1.156
    elif k == 4 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.089
            elif j == 2:
                correction = 1.194
            elif j == 3:
                correction = 1.216
            elif j == 4:
                correction = 1.064
    elif k == 1 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.191
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.105
            elif j == 3:
                correction = 1.143
            elif j == 4:
                correction = 1.168
        elif i == 3:
            if j == 1:
                correction = 1.085
            elif j == 2:
                correction = 1.093
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.069
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.238
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.148
            elif j == 3:
                correction = 1.195
            elif j == 4:
                correction = 1.230
        elif i == 3:
            if j == 1:
                correction = 1.132
            elif j == 2:
                correction = 1.160
            elif j == 3:
                correction = 1.183
            elif j == 4:
                correction = 1.210
        elif i == 4:
            if j == 1:
                correction = 1.118
            elif j == 2:
                correction = 1.116
            elif j == 3:
                correction = 1.150
            elif j == 4:
                correction = 1.185
    elif k == 3 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.232
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.206
            elif j == 3:
                correction = 1.210
            elif j == 4:
                correction = 1.238
        elif i == 3:
            if j == 1:
                correction = 1.144
            elif j == 2:
                correction = 1.178
            elif j == 3:
                correction = 1.226
            elif j == 4:
                correction = 1.216
        elif i == 4:
            if j == 1:
                correction = 1.117
            elif j == 2:
                correction = 1.155
            elif j == 3:
                correction = 1.178
            elif j == 4:
                correction = 1.167
    elif k == 4 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.024
            elif j == 2:
                correction = 1.025
            elif j == 3:
                correction = 1.162
            elif j == 4:
                correction = 1.142
    return correction

