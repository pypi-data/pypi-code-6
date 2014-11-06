#-*- coding: utf-8 -*-#
""" 함수 모듈 """
def print_lol(the_list, level):
	""" 이 함수는 the_list라는 이름의 인자를 갖고 있으며, 파이썬 리스트를 받습니다. 
	이 리스트는 리스트도 항목으로 포함할 수 있습니다. 매 라인마다 리스트에 있는 항목이 
	하나씩 재귀적으로 화면에 출력됩니다. 
	두번째 인자는 중첩된 리스트에서 탭을 추가하기 위해 사용됩니다."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
        	for tab_stop in range(level):
        		print("\t", end='');
            print(each_item)