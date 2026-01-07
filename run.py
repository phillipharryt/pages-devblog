from utils import *
def compile():
    """
    #### Inputs:
        - None 
    #### Expected Behaviour:
        - goes into the list of directories in the posts folder,
            each one is considered a category 
        - inside each directory each post is added to a list
    """
    category_list = build_category_list()
    for each in category_list:
        generate_category_page(each)
    sidebar_soup = build_sidebar_soup(category_list)
    add_sidebar_to_all_posts(sidebar_soup)
    # add_stylesheet_to_all_files()
    add_recent_posts_to_homepage()

    
if __name__ == '__main__':
    func_name = sys.argv[1]
    func = globals()[func_name]
    remaining_args = sys.argv[2:]
    func(*remaining_args)