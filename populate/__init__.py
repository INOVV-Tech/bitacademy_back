from populate.home_coins import populate_home_coins
from populate.free_material import populate_free_materials
from populate.course import populate_courses
from populate.news import populate_news
from populate.tool import populate_tools
from populate.community import populate_community_channels

def populate_primary_entities(home_coins: bool = False, free_materials: bool = False, 
    courses: bool = False, news: bool = False, tools: bool = False, 
    community_channels: bool = False) -> None:
    if home_coins:
        populate_home_coins()

    if free_materials:
        populate_free_materials()
    
    if courses:
        populate_courses()

    if news:
        populate_news()

    if tools:
        populate_tools()

    if community_channels:
        populate_community_channels()