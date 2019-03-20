from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogDB import User, Catalog, CatalogsItem, Base

engine = create_engine('sqlite:///site.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



#
user = User(username="Michael", email="ohayamic@yahoo.co.uk", password="password")
session.add(user)
session.commit()

catalog1 = Catalog(cname="Soccer", user_id=1)
session.add(catalog1)
session.commit()

catItem1 = CatalogsItem(
    name="Shinguards",
    description="Wild pitch bullpen catcher second baseman bases loaded, outs sacrifice hit by pitch count. Disabled list at-bat hot dog mustard ball rainout 4-bagger. Glove pennant sidearm squeeze series reds squeeze. Chin music contact bleeder right fielder choke up range league fair rope.",
    price="$7.50",
    user_id=1,
    catalogs=catalog1,
)
session.add(catItem1)
session.commit()


catItem3 = CatalogsItem(
    name="Jersey",
    description="Center fielder mound 4-6-3 game game full count series in the hole double switch. Dodgers wild pitch outside wild pitch starting pitcher on deck run batted in right fielder.",
    price="$7.50",
    user_id=1,
    catalogs=catalog1,
)
session.add(catItem3)
session.commit()

catItem4 = CatalogsItem(
    name="Soccer Cleats",
    description="Umpire fair bleeder alley fastball stadium pitchout. Starting pitcher right fielder unearned run double switch inning foul loss. On deck fielder's choice game mound pinch hitter, rally batter's box. Team foul pole loss baltimore chop in the hole manager gapper sweep.",
    price="$7.50",
    user_id=1,
    catalogs=catalog1,
)
session.add(catItem4)
session.commit()


catalog2 = Catalog(cname="BaseBall", user_id=1)
session.add(catalog2)
session.commit()

catItem5 = CatalogsItem(
    name="Ball-Stick",
    description="Swing wins 1-2-3 on deck peanuts game ejection rope. Right fielder small ball range foul left field plate ground ball. Loss wrigley tapper rubber gold glove dodgers outfielder field tossed.",
    price="$7.50",
    user_id=1,
    catalogs=catalog2,
)
session.add(catItem5)
session.commit()

catItem2 = CatalogsItem(
    name="Two shinguards",
    description="First base manager rotation series foul line left on base stretch. Stadium on deck first baseman fielder's choice fielder's choice outside stadium rotation.",
    price="$7.50",
    user_id=1,
    catalogs=catalog2,
)
session.add(catItem2)
session.commit()

catalog3 = Catalog(cname="Basketball", user_id=1)
session.add(catalog3)
session.commit()

catItem6 = CatalogsItem(
    name="Canvas",
    description="Base passed ball appeal tossed outs, triple play sport. Fielder's choice designated hitter walk off shift warning track double switch stretch rubber. Butcher boy doubleheader outfield play relay triple play fenway peanuts.",
    price="$7.50",
    user_id=1,
    catalogs=catalog3,
)
session.add(catItem6)
session.commit()


catalog4 = Catalog(cname="Frisbee", user_id=1)
session.add(catalog4)
session.commit()

catItem7 = CatalogsItem(
    name="Stick",
    description="Double play triple play yankees banx mitt save world series pinch hit fall classic. Play backstop leather 4-6-3 force force bunt sacrifice wrigley. Forkball basehit losses slider hey batter, dead ball era bases loaded check swing outs.",
    price="$7.50",
    user_id=1,
    catalogs=catalog4,
)
session.add(catItem7)
session.commit()


catalog5 = Catalog(cname="Snowboarding", user_id=1)
session.add(catalog5)
session.commit()
###
catItem8 = CatalogsItem(
    name="Googles",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    price="$7.50",
    user_id=1,
    catalogs=catalog5,
)
session.add(catItem8)
session.commit()

catItem9 = CatalogsItem(
    name="Snowboard",
    description="Batter's box rally tigers pickoff wrigley rubber game wrigley rubber game wrigley. Outs starter fan moneyball dodgers first base left field fall classic cubs. Glove rope second base third base hit by pitch steal relief pitcher.",
    price="$7.50",
    user_id=1,
    catalogs=catalog5,
)
session.add(catItem9)
session.commit()


catalog6 = Catalog(cname="Rock Climbing", user_id=1)
session.add(catalog6)
session.commit()

catItem10 = CatalogsItem(
    name="Climbing Shoes",
    description="Outfielder cup of coffee base harll left fielder rubber game warning track. Foul line chin music starter triple-A friendly confines, arm balk.",
    price="$7.50",
    user_id=1,
    catalogs=catalog6,
)
session.add(catItem10)
session.commit()


catalog7 = Catalog(cname="Foosball", user_id=1)
session.add(catalog7)
session.commit()

catItem11 = CatalogsItem(
    name="Ball",
    description="Rotation 4-bagger outfielder foul mitt strikeout rake series shutout. Club first base blue alley retire harll season.",
    price="$7.50",
    user_id=1,
    catalogs=catalog7,
)
session.add(catItem11)
session.commit()


catalog8 = Catalog(cname="Skating", user_id=1)
session.add(catalog8)
session.commit()

catItem12 = CatalogsItem(
    name="Hose",
    description="Check swing cup of coffee backstop tapper golden sombrero loogy swing fan knuckleball. Small ball strikeout triple-A foul gold glove gap blue doubleheader.",
    price="$7.50",
    user_id=1,
    catalogs=catalog8,
)
session.add(catItem12)
session.commit()


catalog9 = Catalog(cname="Hockey", user_id=1)
session.add(catalog9)
session.commit()

catItem13 = CatalogsItem(
    name="Hockey Shoes",
    description="I personally cannot get enough baseball. Give this shameless knock-off of Bacon Ipsum a try!",
    price="$7.50",
    user_id=1,
    catalogs=catalog9,
)
session.add(catItem13)
session.commit()
