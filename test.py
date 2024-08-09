import sys
print(sys.path)


class TestClass:
    def test_0(self):
        
        
        
            s1 = 'TheQueensMedicalCenter'
    s2 = 'QUEENSMEDICALCENTER'
    
    print(len(s1))
    print(len(s2))
    print(jarowinkler_similarity(s1,s2))
    print(jarowinkler_similarity(s1,s2, score_cutoff=0.9))
    print(JW_score(s1,s2))
    print(JW_score2(s1,s2, 1000,4,1)) # TODO : check what those variables are
    print("--------------------------------------------")
    s1 = '2251CORPORATEPARKDR'
    s2 = '2251CORPORATEPARKDRSTE300'
    print(jarowinkler_similarity(s1,s2))
    print(jarowinkler_similarity(s1,s2, score_cutoff=0.9))
    print(JW_score(s1,s2))
    print(JW_score2(s1,s2, 0.1, 3)) # TODO : check what those variables are