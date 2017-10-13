from tests.bootstrap.test_bootstrap import *

article1 = """
Team17 announced today that it’ll publish Pathea Games’s My Time at Portia, a colorful open-world role-playing game. This marks its first partnership with a Chinese studio, and it follows an announcement earlier this year about the first time it signed on with a Brazilian developer. My Time at Portia is raising money on the crowdfunding platform Kickstarter, and aims to be in early access in 2018. It will be available on PC and Mac to start, and Team17 will help bring the game to consoles later on.

Debbie Bestwick, Team17’s CEO, said that China has been on their radar for quite some time. It’s also turned into a country where their games do very well. This year, they’ve seen a big increase in revenue from China, and a lot of interest in their new title Escapists 2. 25 percent of Escapists 2 players are Chinese.

“We’ve had a huge fivefold increase in revenues in a year for that market,” said Bestwick in a phone call with GamesBeat. “Escapists 2 launched 22nd of August this year. On Steam it was the No. 1 best-selling new release in August, for the whole month. Looking at China, in terms of unit sales, China is our number one market.”

Bestwick said there’s an exciting indie scene in China, and she and her team have been looking for studios to partner with. They knew of Pathea because of its first title, Planet Explorers, which released late last year on Steam and sold 300,000 copies. A lot of her team had tried My Time at Portia’s demo, which is available to download for free and promises six to eight hours of gameplay — virtually unheard of for a demo.

“I don’t know the exact hours, but it’s somewhere between 30 and 40 when it launches in early access,” said Bestwick. “This is a very deep game. The production values are outstanding. If I wanted to get anything over to you, I would try to get across the quality of this studio. This is not a tiny little team that have never made a game before.”

Pathea is a 57-person studio based in Chongqing, China. It was founded in 2012, and it began working on My Time at Portia in 2015.

“From the start, we were influenced heavily by Hayao Miyazaki’s Future Boy Conan and Nausicaa, and games like Dark Cloud 2, Harvest Moon, and Steambot Chronicles,” said Zifei Wu, Pathea’s president, in an email. “In the world of My Time at Portia, the world sadly came to an end in war and darkness over 330 years ago. Around 100 years ago, humans picked up the pieces and begin to rebuild society again.”

Wu said that they’re seeking to create a dynamic world where the player’s actions have an effect. The player can develop friendships or romances with non-playable characters, in addition to the farming, crafting, fighting, and fishing that’s expected in this kind of open-world game. NPCs can change, get new jobs, or leave town depending on the way the player acts.

Though Pathea’s previous title Planet Explorers sold a decent number of copies on Steam, Wu said that the biggest challenge for Chinese developers is reaching a Western audience. Partnering with Team17 could help alleviate this, as the publisher has experience with catering to global markets.

“The biggest problem though for indies in China is that the main market for indie games is the West, mostly on Steam, and most Chinese studios have no idea how to market to that market,” said Wu. “A lot of times, they completely ignore the rest of the players on Steam and only go for that Chinese segment. This can hurt the bottom line quite a bit.”

This year, North America will generate $27 billion in gaming revenue, according to industry analyst Newzoo. This is overshadowed by the Asia-Pacific region, which altogether will generate $51.2 billion. In that region, China is massive and will account for $27.5 billion of revenue on its own.

Still, the marketing problem is only part of the set of challenges facing indie devs in China. Wu said that funding is another issue, since investors often want huge returns that indie studios simply can’t deliver. There’s also brain drain, with many folks opting to work for huge companies like Tencent and NetEase, which are both enormous players and have been jostling at the top of the mobile charts.

“Indie companies can’t compete with their salaries; last year the average salary/bonus at Tencent was around $125,000, we can’t beat that,” said Wu. “Still, even with all these problems, the indie game scene has been booming the last couple of years in China. There are now conventions and game jams all the time. We think this is just the start and you’ll see more and bigger Chinese games on the horizon.”

"""

article2 = """
 Uber’s top boss in Britain will quit the taxi hailing app just as the firm battles to overturn a decision to strip it of its license in London, according to an email seen by Reuters.

The British capital’s transport regulator deemed Uber unfit to run a taxi web last month and decided not to renew its license to operate, citing the firm’s approach to reporting serious criminal offences and background checks on drivers.

But in an email seen by Reuters on Monday, Uber’s Northern European Manager Jo Bertram, who has responsibility for Britain among other countries, said the firm needed a new manager in the region to tackle the issues it faces.

“Given some of our current challenges, I’m also convinced that now is the right time to have a change of face, and to hand over to someone who will be here for the long haul and take us into the next phase,” she said.

In response, Uber’s top boss in Europe, the Middle East and Africa said that the firm would now seek out Bertram’s replacement.

“Jo will remain with us over the next few weeks in order to help with a smooth transition, and I look forward to working closely with the excellent team she leaves behind,” Pierre-Dimitri Gore-Coty said in an email seen by Reuters.

The firm’s London boss Tom Elvidge will head up UK operations on an interim basis, he said.

Uber’s new global Chief Executive Dara Khosrowshahi is due in London on Tuesday to meet the head of the city’s transport regulator in a bid to keep operating in one of its most important foreign markets.

Bertram heads up the San Francisco-based app’s operations in ten countries including Britain, Ireland, Belgium, the Netherlands and Luxembourg.

In the email, she declined to say where she would be moving to.

“An exciting new opportunity has arisen that will allow me to apply what I’ve learnt here and I’ll be able to share more details with you soon,” she said.

"""


def show_related_articles(facade, article):
    #related_articles_doc2vec = facade.get_related_articles(article, 10000)
    related_articles = facade.get_related_articles_in_interval(article, n=10000, reference_day=None, days=20, max=15)

    print(" ==== related_articles  ==== ")
    print(related_articles)

show_related_articles(doc2VecFacade, article1)
show_related_articles(doc2VecFacade, article2)


show_related_articles(tfidfFacade, article1)
show_related_articles(tfidfFacade, article2)

