def sum_timestamps(times: list) -> str:
    h_tot = m_tot = s_tot = 0
    for tm in times:
        *m, s = [int(v) for v in tm.split(':')]
        if len(m) > 1:
            h_tot += m[0]
        m_tot += m[-1]
        s_tot += s
        if s_tot > 59:
            m_tot += 1
            s_tot -= 60
        if m_tot > 59:
            h_tot += 1
            m_tot -= 60
    if h_tot > 0:
        return f'{h_tot}:{m_tot:02}:{s_tot:02}'
    return f'{m_tot}:{s_tot:02}'
