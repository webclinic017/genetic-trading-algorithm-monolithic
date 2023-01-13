import numpy as np

def P1_Range(P1_min, P1_max, P1_cut):
    P1_step  = int((P1_max - P1_min) /P1_cut)
    range_P1 = np.arange(P1_min, P1_max+1, P1_step)
    return range_P1, P1_step

def P2_Range(P2_min, P2_max, P2_cut):
    P2_step  = int((P2_max - P2_min) /P2_cut)
    range_P2 = np.arange(P2_min, P2_max+1, P2_step)
    return range_P2, P2_step

def P3_Range(P3_min, P3_max, P3_cut):
    P3_step  = int((P3_max - P3_min) /P3_cut)
    range_P3 = np.arange(P3_min, P3_max+1, P3_step)
    return range_P3, P3_step

def P4_Range(P4_min, P4_max, P4_cut):
    P4_step = int((P4_max - P4_min) / P4_cut)
    range_P4 = np.arange(P4_min, P4_max+1, P4_step)
    return range_P4, P4_step
#____________________________________________________________

def create_BEST_params_list(df_result):
    # FIXME: 
    df_result = df_result.sort_values(by="GAIN_SUM", ascending=False)
    df_result.reset_index(drop=True, inplace=True)

    list_bestParams = df_result.loc[0,"PARAMS"]

    return list_bestParams
#____________________________________________________________

def best_P1_Range(P1_step_1st, P1_BEST_1st, P1_cut_2nd):

    if P1_BEST_1st < P1_step_1st:
        P1_min_2nd = P1_BEST_1st
    else:
        P1_min_2nd = P1_BEST_1st - P1_step_1st

    P1_max_2nd   = P1_BEST_1st + P1_step_1st
    P1_step_2nd  = int((P1_max_2nd - P1_min_2nd)/P1_cut_2nd)
    P1_range_2nd = np.arange(P1_min_2nd, P1_max_2nd + 1, P1_step_2nd)

    return P1_range_2nd


def best_P2_Range(P2_step_1st, P2_BEST_1st, P2_cut_2nd):

    if P2_BEST_1st < P2_step_1st:
        P2_min_2nd = P2_BEST_1st
    else:
        P2_min_2nd = P2_BEST_1st - P2_step_1st

    P2_max_2nd   = P2_BEST_1st + P2_step_1st
    P2_step_2nd  = int((P2_max_2nd - P2_min_2nd)/P2_cut_2nd)
    P2_range_2nd = np.arange(P2_min_2nd, P2_max_2nd + 1, P2_step_2nd)

    return P2_range_2nd


def best_P3_Range(P3_step_1st, P3_BEST_1st, P3_cut_2nd):

    if P3_BEST_1st < P3_step_1st:
        P3_min_2nd = P3_BEST_1st
    else:
        P3_min_2nd = P3_BEST_1st - P3_step_1st

    P3_max_2nd   = P3_BEST_1st + P3_step_1st
    P3_step_2nd  = int((P3_max_2nd - P3_min_2nd)/P3_cut_2nd)
    P3_range_2nd = np.arange(P3_min_2nd, P3_max_2nd + 1, P3_step_2nd)

    return P3_range_2nd


def best_P4_Range(P4_step_1st, P4_BEST_1st, P4_cut_2nd):

    if P4_BEST_1st < P4_step_1st:
        P4_min_2nd = P4_BEST_1st
    else:
        P4_min_2nd = P4_BEST_1st - P4_step_1st

    P4_max_2nd   = P4_BEST_1st + P4_step_1st
    P4_step_2nd  = int((P4_max_2nd - P4_min_2nd)/P4_cut_2nd)
    P4_range_2nd = np.arange(P4_min_2nd, P4_max_2nd + 1, P4_step_2nd)

    return P4_range_2nd