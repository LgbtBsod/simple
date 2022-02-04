def md(e, key):
    if not e:
        return
    m_k = e[0][key]
    m_e = e[0]

    for x in e:
        if x[key] > m_k:
            m_k = x[key]
       
            m_e = e
    return m_e


def filters_d(e, key, m_v):
    new_m = []
    for x in e:
        if x[key] >= m_v:
            new_m.append(x)
    return new_m
