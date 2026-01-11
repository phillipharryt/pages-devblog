from utils import Utils
import sys
def compile():
    """
    #### Inputs:
        - None 
    #### Expected Behaviour:
        - goes into the list of directories in the posts folder,
            each one is considered a category 
        - inside each directory each post is added to a list
    """
    instance = Utils()
    instance.GITHUB_URL = ''
    _shared_compile(instance)
   
    
def compile_for_github(github_url: str):
    instance = Utils()
    instance.GITHUB_URL = github_url
    _shared_compile(instance)
    
def _shared_compile(instance: Utils):
    category_list = Utils.build_category_list()
    for each in category_list:
        instance.generate_category_page(each)
    sidebar_soup = instance.build_sidebar_soup(category_list)
    Utils.add_sidebar_to_all_posts(sidebar_soup)
    # add_stylesheet_to_all_files()
    instance.add_recent_posts_to_homepage()

    
if __name__ == '__main__':
    func_name = sys.argv[1]
    func = globals()[func_name]
    remaining_args = sys.argv[2:]
    func(*remaining_args)