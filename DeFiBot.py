import tweepy
import json # The API returns JSON formatted text
import urllib.request as urllib2
import re
import requests
import random


# Store OAuth authentication credentials - get at https://developer.twitter.com/en/apps
access_token = "111111111111111-11111111111111111111"
access_token_secret = "11111111111111111111111111111111111"
consumer_key = "aaaaaaaaaaaaaaaaaaaaaa"
consumer_secret = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
passphrase = "your passphrase"

#Bad words source https://github.com/MauriceButler/badwords
badwords = ["4r5e", "5h1t", "5hit", "a55", "anal", "anus", "ar5e", "arrse", "arse", "ass", "ass-fucker", "asses", "assfucker", "assfukka", "asshole", "assholes", "asswhole", "a_s_s", "b!tch", "b00bs", "b17ch", "b1tch", "ballbag", "balls", "ballsack", "bastard", "beastial", "beastiality", "bellend", "bestial", "bestiality", "bi+ch", "biatch", "bitch", "bitcher", "bitchers", "bitches", "bitchin", "bitching", "bloody", "blow job", "blowjob", "blowjobs", "boiolas", "bollock", "bollok", "boner", "boob", "boobs", "booobs", "boooobs", "booooobs", "booooooobs", "breasts", "buceta", "bugger", "bum", "bunny fucker", "butt", "butthole", "buttmuch", "buttplug", "c0ck", "c0cksucker", "carpet muncher", "cawk", "chink", "cipa", "cl1t", "clit", "clitoris", "clits", "cnut", "cock", "cock-sucker", "cockface", "cockhead", "cockmunch", "cockmuncher", "cocks", "cocksuck", "cocksucked", "cocksucker", "cocksucking", "cocksucks", "cocksuka", "cocksukka", "cok", "cokmuncher", "coksucka", "coon", "cox", "crap", "cum", "cummer", "cumming", "cums", "cumshot", "cunilingus", "cunillingus", "cunnilingus", "cunt", "cuntlick", "cuntlicker", "cuntlicking", "cunts", "cyalis", "cyberfuc", "cyberfuck", "cyberfucked", "cyberfucker", "cyberfuckers", "cyberfucking", "d1ck", "damn", "dick", "dickhead", "dildo", "dildos", "dink", "dinks", "dirsa", "dlck", "dog-fucker", "doggin", "dogging", "donkeyribber", "doosh", "duche", "dyke", "ejaculate", "ejaculated", "ejaculates", "ejaculating", "ejaculatings", "ejaculation", "ejakulate", "f u c k", "f u c k e r", "f4nny", "fag", "fagging", "faggitt", "faggot", "faggs", "fagot", "fagots", "fags", "fanny", "fannyflaps", "fannyfucker", "fanyy", "fatass", "fcuk", "fcuker", "fcuking", "feck", "fecker", "felching", "fellate", "fellatio", "fingerfuck", "fingerfucked", "fingerfucker", "fingerfuckers", "fingerfucking", "fingerfucks", "fistfuck", "fistfucked", "fistfucker", "fistfuckers", "fistfucking", "fistfuckings", "fistfucks", "flange", "fook", "fooker", "fuck", "fucka", "fucked", "fucker", "fuckers", "fuckhead", "fuckheads", "fuckin", "fucking", "fuckings", "fuckingshitmotherfucker", "fuckme", "fucks", "fuckwhit", "fuckwit", "fudge packer", "fudgepacker", "fuk", "fuker", "fukker", "fukkin", "fuks", "fukwhit", "fukwit", "fux", "fux0r", "f_u_c_k", "gangbang", "gangbanged", "gangbangs", "gaylord", "gaysex", "goatse", "God", "god-dam", "god-damned", "goddamn", "goddamned", "hardcoresex", "hell", "heshe", "hoar", "hoare", "hoer", "homo", "hore", "horniest", "horny", "hotsex", "jack-off", "jackoff", "jap", "jerk-off", "jism", "jiz", "jizm", "jizz", "kawk", "knob", "knobead", "knobed", "knobend", "knobhead", "knobjocky", "knobjokey", "kock", "kondum", "kondums", "kum", "kummer", "kumming", "kums", "kunilingus", "l3i+ch", "l3itch", "labia", "lust", "lusting", "m0f0", "m0fo", "m45terbate", "ma5terb8", "ma5terbate", "masochist", "master-bate", "masterb8", "masterbat*", "masterbat3", "masterbate", "masterbation", "masterbations", "masturbate", "mo-fo", "mof0", "mofo", "mothafuck", "mothafucka", "mothafuckas", "mothafuckaz", "mothafucked", "mothafucker", "mothafuckers", "mothafuckin", "mothafucking", "mothafuckings", "mothafucks", "mother fucker", "motherfuck", "motherfucked", "motherfucker", "motherfuckers", "motherfuckin", "motherfucking", "motherfuckings", "motherfuckka", "motherfucks", "muff", "mutha", "muthafecker", "muthafuckker", "muther", "mutherfucker", "n1gga", "n1gger", "nazi", "nigg3r", "nigg4h", "nigga", "niggah", "niggas", "niggaz", "nigger", "niggers", "nob", "nob jokey", "nobhead", "nobjocky", "nobjokey", "numbnuts", "nutsack", "orgasim", "orgasims", "orgasm", "orgasms", "p0rn", "pawn", "pecker", "penis", "penisfucker", "phonesex", "phuck", "phuk", "phuked", "phuking", "phukked", "phukking", "phuks", "phuq", "pigfucker", "pimpis", "piss", "pissed", "pisser", "pissers", "pisses", "pissflaps", "pissin", "pissing", "pissoff", "poop", "porn", "porno", "pornography", "pornos", "prick", "pricks", "pron", "pube", "pusse", "pussi", "pussies", "pussy", "pussys", "rectum", "retard", "rimjaw", "rimming", "s hit", "s.o.b.", "sadist", "schlong", "screwing", "scroat", "scrote", "scrotum", "semen", "sex", "sh!+", "sh!t", "sh1t", "shag", "shagger", "shaggin", "shagging", "shemale", "shi+", "shit", "shitdick", "shite", "shited", "shitey", "shitfuck", "shitfull", "shithead", "shiting", "shitings", "shits", "shitted", "shitter", "shitters", "shitting", "shittings", "shitty", "skank", "slut", "sluts", "smegma", "smut", "snatch", "son-of-a-bitch", "spac", "spunk", "s_h_i_t", "t1tt1e5", "t1tties", "teets", "teez", "testical", "testicle", "tit", "titfuck", "tits", "titt", "tittie5", "tittiefucker", "titties", "tittyfuck", "tittywank", "titwank", "tosser", "turd", "tw4t", "twat", "twathead", "twatty", "twunt", "twunter", "v14gra", "v1gra", "vagina", "viagra", "vulva", "w00se", "wang", "wank", "wanker", "wanky", "whoar", "whore", "willies", "willy", "xrated", "xxx"]
nicewords = ["fomo", "moon", "alien", "aliens", "zark", "defi", "magic", "ardor", "ignis", "nxt", "jelurida", "able", "abundance", "accelerate", "accept", "acclaim", "accomplish", "accrue", "ace", "accord", "achieve", "action", "accolade", "accredit", "activate", "active", "add", "addition", "adept", "admirable", "adorable", "advance", "advantage", "adventure", "affable", "affirm", "ageless", "agree", "agreeable", "aid", "aim", "alacrity", "alert", "alight", "alive", "all", "right", "always", "amaze", "amazing", "amiable", "ambition", "amity", "amuse", "anew", "appealing", "applaud", "appreciate", "aspire", "approve", "arouse", "ascend", "assent", "assert", "assist", "associate", "assure", "astir", "astonish", "attain", "attempt", "attentive", "attest", "attraction", "attribute", "attune", "augment", "auspicious", "authentic", "available", "avid", "awake", "award", "aware", "awash", "awesome", "aye", "beatific", "beatify", "beatitude", "beauteous", "beautiful", "beautify", "benefaction", "beneficial", "befriend", "benefit", "benevolent", "beauty", "beloved", "best", "bestow", "better", "betterment", "big", "bijou", "bless", "blessed", "blessing", "bliss", "bloom", "blossom", "bonafide", "bonanza", "bonus", "boost", "bountiful", "bounty", "bright", "brighten", "brill", "brilliant", "bubbly", "budding", "buddy", "build", "calm", "can", "capable", "care", "celebrate", "certain", "charitable", "charity", "charm", "charmer", "charming", "cheerful", "cheers", "chirp", "chirpy", "choice", "chortle", "chuckle", "cinch", "civility", "classy", "clean", "clear", "comely", "comfort", "comfortable", "comic", "comical", "compliment", "confidence", "confirm", "congenial", "congratulate", "conscious", "consciousness", "consider", "considerate", "constant", "constructive", "content", "contribute", "cool", "cooperate", "cope", "cordial", "correct", "cosy", "could", "courage", "courteous", "creative", "credit", "cuddly", "cushy", "cute", "decency", "decent", "delectable", "delicate", "delicious", "delight", "desirable", "do", "dreamy", "dynamic", "eager", "ease", "easily", "easy", "economic", "ecstasy", "edify", "educate", "effective", "efficiency", "efficient", "elate", "elegant", "elevate", "eligible", "emphasis", "emphasize", "emphatic", "enable", "enchant", "encourage", "endear", "endearment", "endeavour", "endorse", "endow", "energetic", "energize", "energy", "engage", "engaging", "engross", "enhance", "enjoy", "enlighten", "enlist", "enliven", "enormous", "enough", "enrapture", "enrich", "ensure", "enterprise", "enterprising", "entertain", "entertainment", "enthral", "enthuse", "enthusiasm", "enthusiastic", "entire", "entrust", "equal", "equality", "equally", "equilibrium", "equitable", "equity", "equivalent", "erudite", "especial", "essence", "essential", "establish", "esteem", "ethic", "ethical", "euphony", "euphoria", "eureka", "evolution", "exalt", "exceed", "exceedingly", "excel", "excellence", "excellent", "excite", "exotic", "expert", "expertise", "exquisite", "extensive", "extraordinary", "exult", "fabulous", "fair", "faith", "faithful", "fame", "family", "fancy", "fantastic", "fare", "fascinate", "fast", "favour", "favourite", "feasible", "felicity", "fellowship", "festive", "fetching", "fine", "finesse", "first", "fit", "fitting", "flamboyant", "flash", "flexible", "flower", "focus", "fond", "fondly", "for", "foresee", "foresight", "forever", "forgive", "forgiveness", "forward", "frank", "free", "freedom", "fresh", "friend", "friendly", "friendship", "fruitful", "fulfil", "fully", "fun", "funny", "gallant", "galore", "game", "generate", "generous", "genial", "genius", "gentle", "genuine", "gift", "gifted", "giggle", "gist", "give", "glad", "glorious", "glory", "glossy", "glow", "go", "going", "good", "goodness", "goodwill", "gorgeous", "gosh", "grace", "graceful", "gracious", "grand", "grandeur", "grateful", "gratify", "gratitude", "great", "greet", "greeting", "grow", "guarantee", "guest", "guidance", "guide", "handy", "happily", "happy", "harmonious", "harmonize", "harmony", "healthy", "heart", "heaven", "heavenly", "hello", "help", "helpful", "helping", "highly", "hilarious", "hilarity", "hip", "holy", "homely", "honest", "honestly", "honesty", "honeyed", "honorary", "honour", "honourable", "hooray", "hope", "hopeful", "hopefully", "hospitable", "hot", "humane", "humanitarian", "humorous", "humour", "idea", "ideal", "ideally", "immense", "immerse", "immune", "impartial", "impeccable", "impress", "impressive", "improve", "improvement", "increase", "incredible", "indeed", "ingenious", "ingenuity", "initiate", "initiative", "innocent", "innovate", "input", "inspiration", "inspire", "inspired", "interest", "interested", "interesting", "invitation", "invite", "inviting", "jest", "joke", "jolly", "jovial", "joy", "joyful", "joyous", "jubilant", "jubilation", "juicy", "just", "keen", "keep", "up", "kind", "kind-hearted", "kindly", "kiss", "kudos", "large", "lark", "laugh", "lavish", "learn", "learned", "learning", "leisure", "leisured", "leisurely", "liberate", "liberation", "life", "light", "lighten", "light-hearted", "likable", "like", "liking", "lively", "lovable", "love", "lovely", "loving", "loyal", "lucid", "luck", "lucky", "lucrative", "luminous", "luscious", "lush", "lustre", "lustrous", "luxuriant", "luxuriate", "luxurious", "luxury", "made", "magnificent", "magnify", "magnitude", "maintain", "majesty", "major", "majority", "make", "manage", "manifest", "manner", "many", "marvellous", "master", "matter", "mediate", "meditate", "mellow", "mercy", "merit", "method", "miracle", "miraculous", "morale", "most", "motivate", "much", "multitude", "must", "neat", "new", "newly", "nice", "nicety", "nifty", "nippy", "nirvana", "noble", "nod", "normal", "notable", "note", "noted", "notice", "noticeable", "nourish", "now", "nurse", "nurture", "obliging", "offer", "ok", "on", "onward", "oodles", "oomph", "open", "openly", "open-minded", "opportune", "opportunity", "original", "outgoing", "outstanding", "pacify", "palatable", "palpable", "paradise", "paragon", "pardon", "par", "excellence", "passion", "passionate", "passive", "patience", "patient", "peace", "peaceable", "peaceful", "peak", "pep", "perfect", "perfection", "practical", "praise", "precious", "prize", "pro", "produce", "productive", "proficient", "progress", "promote", "promotion", "prosper", "pukka", "pure", "purify", "purity", "persevere", "perspective", "placid", "pleasant", "please", "pleasurable", "pleasure", "plenitude", "plenteous", "plenty", "plus", "plush", "poise", "polite", "positive", "possible", "potential", "quality", "quiet", "radiant", "rapture", "ready", "real", "really", "reason", "reassure", "receive", "reception", "receptive", "reciprocate", "recommend", "refreshing", "regard", "relax", "release", "reliable", "relief", "remarkable", "remedy", "reputable", "respect", "responsible", "rest", "restful", "restore", "result", "reward", "rewarding", "rich", "richly", "right", "sacred", "sacrosanct", "safe", "safety", "salubrious", "satisfaction", "satisfactory", "satisfy", "save", "saving", "saviour", "self-assertive", "self-confidence", "self-discipline", "self-esteem", "self-help", "sense", "sensible", "share", "simple", "simplicity", "simplify", "simply", "sincere", "smart", "smashing", "smile", "sociable", "social", "special", "spectacular", "splendid", "splendiferous", "splendour", "steady", "straightforward", "succeed", "success", "successful", "succinct", "suffice", "sufficiency", "sufficient", "sumptuous", "super", "superabundant", "super", "superior", "supple", "supply", "support", "supporter", "supporting", "supportive", "supreme", "sure", "sweet", "swell", "swift", "sympathetic", "sympathise", "sympathy", "tact", "teach", "teacher", "teaching", "team", "testament", "testimonial", "testimony", "thank", "thankful", "thanksgiving", "therapeutic", "therapy", "thorough", "thoughtful", "thrill", "thrive", "tidy", "timeless", "timely", "top", "training", "tranquil", "tranquillity", "transcend", "transient", "transparent", "triumph", "triumphant", "true", "trust", "trustworthy", "trusty", "truth", "try", "tuition", "ultimate", "ultra", "unconditional", "uncritical", "understand", "understanding", "unequalled", "unequivocal", "unerring", "unfetter", "unflagging", "ungrudging", "upbeat", "upgrade", "uplift", "upstanding", "urbane", "useful", "user-friendly", "utmost", "valid", "validate", "valuable", "value", "venerable", "veracious", "verify", "versatile", "very", "viable", "vibrant", "virtue", "virtuosity", "virtuoso", "virtuous", "vitality", "vivacious", "vivid", "warm", "warmth", "welcome", "well", "wellbeing", "wholehearted", "wholesome", "wholly", "will", "willing", "win", "winner", "winning", "winsome", "wisdom", "wise", "with", "witty", "won", "wonder", "wonderful", "wonderment", "wondrous", "workable", "worth", "worthwhile", "worthy", "would", "wow", "yea", "yeah", "yearn", "yes", "yippee", "young", "youth", "youthful", "zeal", "zealous", "zest"]

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

TRACKING_KEYWORDS = ['#DeFiMagic']
OUTPUT_FILE = "bot_tweets.txt"
TWEETS_TO_CAPTURE = 3000000


class MyStreamListener(tweepy.StreamListener):
    """
    Twitter listener, watching for tweets with the tracking keyword
    """
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open(OUTPUT_FILE, "w")
    
    global cnt
    global users
    global users2
    global usermessaged
    global ardoraccounts
    global addresslenght
    
    cnt = 0
    users = []
    users2 = []
    usermessaged = []
    ardoraccounts = []

    def on_status(self, status):
        global cnt
        tweet = status._json
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        
        #According to the Bot triggers, calculate the initial DeFi amount
        
        if self.num_tweets <= TWEETS_TO_CAPTURE:
            if cnt > 25600:
                amount = 10000;
            if cnt <= 25600:
                amount = 390625;
            if cnt <= 12800:
                amount = 781250;
            if cnt <= 6400:
                amount = 1562500;
            if cnt <= 3200:
                amount = 3125000;
            if cnt <= 1600:
                amount = 6250000;
            if cnt <= 800:
                amount = 12500000;
            if cnt <= 400:
                amount = 25000000;
            if cnt <= 200:
                amount = 50000000;
            if cnt <= 100:
                amount = 100000000;
            #logging
            print(tweet);
            #Put tweet text in a variable
            text = tweet['text'];
            #logging
            print(text);
            
            #Find Ardor address in text
            for ArdorAddress in text.split():
                if ArdorAddress.startswith("ARDOR-"):
                    print(ArdorAddress);
                    ArdorAdd = ArdorAddress;
                    addresslenght = len(ArdorAdd)
                    print(addresslenght)
            print(ArdorAdd);
            #create list of words in text
            words = text.split(" ")
            #logging
            print(words)
            #Find matching good words
            matching_good_words = list(set(map(str.lower,words)) & set(nicewords))
            #Find how many good words are in text
            matching_good = len(matching_good_words)
            #logging
            print(matching_good_words)
            print(matching_good)
            #Find matching bad words
            matching_bad_words = list(set(map(str.lower,words)) & set(badwords))
            #Find how many bad words are in text
            matching_bad = len(matching_bad_words)
            #logging
            print(matching_bad_words)
            print(matching_bad)
            #Calculate multiplier for additional Defi
            if (matching_bad == 0) and (matching_good>0):
                multiplier=0.7
            if (matching_good == 0) and (matching_bad>0):
                multiplier= 0
            if (matching_bad!=0) and (matching_good!=0):
                multiplier=0.3
            if (matching_bad ==0) and (matching_good==0):
                multiplier=0.1
            #Add a random 0 - 0.3 random multiplier on top of previous value
            multiplier = multiplier + (0.3 * random.random())
            #logging
            print(multiplier)
            print(amount)
            #Put the amount in another variable
            amountdup = amount
            #calculate the bunus amount rounded to 10000 multiples
            extraamount = round((amount * multiplier) / 10000) * 10000
            amount = round(amount + extraamount)
            #logging
            print(amount)
            #put twitter user in variable user
            user = tweet['user']['screen_name']
            #If user already in the users array then it means that it already triggered the bot once
            if tweet['user']['screen_name'] in users:
                print('User {} already asked for DeFi once'.format(tweet['user']['screen_name']))
                #add to array with twitter user - ardor account couples 
                userarray=[user,ArdorAdd]
                #Send a last message if user already triggered the bot twice
                if (user not in usermessaged) and (user in users2):
                    try:
                        print("Hey @"+tweet['user']['screen_name']+" you already asked for #DeFi on #Ignis. You're already closer than others to the moon. #DeadFish #Ardor")
                        api.update_status(status="Hey @"+tweet['user']['screen_name']+" you and your friend already got #DeFi on #Ignis. You're already half way to the moon. #DeadFish #Ardor");
                        usermessaged.append(user)
                    except Exception as error:
                        print(error)
                    else:
                        #logging
                        print('User already asked for DEFI: {}'.format(tweet['user']['screen_name']))
                #check if user can trigger the bot the second time       
                if (userarray not in ardoraccounts) and (user not in users2) and (addresslenght == 26):
                    try:
                        #Add trigger user to users2 list to track the second triggering of the bot
                        users2.append(tweet['user']['screen_name'])
                        print(str(amount/1000000)+' Second DEFI sent to: {}'.format(tweet['user']['screen_name']))
                        
                        #Get Transaction Fee
                        datain = 'https://localhost:27876/nxt?requestType=transferAsset&secretPhrase='+str(passphrase)+'&chain=ignis&asset=12281945935996100528&recipient='+str(ArdorAdd)+'&quantityQNT='+str(amount)+'&feeNQT=-1&feeRateNQTPerFXT=-1&deadline=60'
                        datain = datain.replace(" ", "%20")
                        
                        result = requests.post(datain)
                        jsondata = json.loads(result.text)
                        #logging
                        print(jsondata)
                        #calculate correct fee
                        rate = int(int(jsondata["bundlerRateNQTPerFXT"]) * 0.01)
                        
                        
                        #Execute Transaction with correct fee
                        datain = 'https://localhost:27876/nxt?requestType=transferAsset&secretPhrase='+str(passphrase)+'&chain=ignis&asset=12281945935996100528&recipient='+str(ArdorAdd)+'&quantityQNT='+str(amount)+'&feeNQT='+str(rate)+'&deadline=60'
                        datain = datain.replace(" ", "%20")
                        
                        result = requests.post(datain)
                        jsondata = json.loads(result.text)
                        #logging
                        print(jsondata)
                       
                    except Exception as error:
                        print(error) 
                    else:
                        #If no exception in transaction execution then send tweets according to multiplier and update variables
                        cnt += 1
                        users.append(tweet['user']['screen_name'])
                        ardoraccounts.append([user,ArdorAdd])
                        print(ardoraccounts)
                        if (multiplier > 0.8):
                            api.update_status(status="Hey @"+tweet['user']['screen_name']+"! That was awesome! Your buddy is one step closer to the moon too! #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on the way! #DeadFish #Ardor")
                            print(str(amount)+' You were awesome to friend Defi sent to: {}'.format(tweet['user']['screen_name']))
                        elif (multiplier < 0.8) and (multiplier > 0.5):
                            api.update_status(status="Hey @"+tweet['user']['screen_name']+"! That was sweet. Your buddy is one step closer to the moon too! #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on the way! #DeadFish #Ardor")
                            print(str(amount)+' You were kind to friend Defi sent to: {}'.format(tweet['user']['screen_name']))
                        else:
                            api.update_status(status="Hey @"+tweet['user']['screen_name']+" that was not so nice. Your buddy is anyway a half step closer to the moon. #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on the way! #DeadFish #Ardor")
                            print(str(amount)+' You were not kind to friend Defi sent to: {}'.format(tweet['user']['screen_name']))
                        #logging to check on screen how many triggers have been executed
                        print(cnt)
                        
                        
                        
                #if twitter user and ardor account are in ardoraccounts array then tweet that this is not ok
                elif (userarray in ardoraccounts) and (user not in usermessaged):
                    print('you already used that address {}'.format(tweet['user']['screen_name']))
                    api.update_status(status="Hey @"+tweet['user']['screen_name']+" you cannot send #DeFi to the same #Ardor account. Be nice and send them to one of your friends! It's all about sharing. #DeadFish #Ignis")
                
            #check if this is first trigger and if ardor address is the correct lenght
            if (tweet['user']['screen_name'] not in users) and (addresslenght == 26):
                try:
                    #see previous comments. Same story here
                    datain = 'https://localhost:27876/nxt?requestType=transferAsset&secretPhrase='+str(passphrase)+'&chain=ignis&asset=12281945935996100528&recipient='+str(ArdorAdd)+'&quantityQNT='+str(amount)+'&feeNQT=-1&feeRateNQTPerFXT=-1&deadline=60'
                    datain = datain.replace(" ", "%20")
                    print(datain)
                    
                    result = requests.post(datain)
                    jsondata = json.loads(result.text) 
                    
                    print(jsondata)
                    rate = int(int(jsondata["bundlerRateNQTPerFXT"]) * 0.01)
                    
                    print(rate)
                    datain = 'https://localhost:27876/nxt?requestType=transferAsset&secretPhrase='+str(passphrase)+'&chain=ignis&asset=12281945935996100528&recipient='+str(ArdorAdd)+'&quantityQNT='+str(amount)+'&feeNQT='+str(rate)+'&deadline=60'
                    datain = datain.replace(" ", "%20")
                    print(datain)
                    
                    result = requests.post(datain)
                    jsondata = json.loads(result.text)
                    
                    print(jsondata)
                    
                    
                except Exception as error:
                    print(error) 
                else:
                    #check previous comments. Same story here
                    cnt += 1
                    users.append(tweet['user']['screen_name'])
                    ardoraccounts.append([user,ArdorAdd])
                    if (multiplier > 0.8):
                        api.update_status(status="Hey @"+tweet['user']['screen_name']+"! That was awesome! You're one step closer to the moon! #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on your way! #DeadFish #Ardor")
                        print(str(amount)+' You were awesome Defi sent to: {}'.format(tweet['user']['screen_name']))
                    elif (multiplier < 0.8) and (multiplier > 0.5):
                        api.update_status(status="Hey @"+tweet['user']['screen_name']+"! That was sweet. You're one step closer to the moon! #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on your way! #DeadFish #Ardor")
                        print(str(amount)+' You were kind Defi sent to: {}'.format(tweet['user']['screen_name']))
                    else:
                        api.update_status(status="Hey @"+tweet['user']['screen_name']+" that was not so nice. You're anyway half a step closer to the moon. #DeFi on #Ignis is the future. BOOM! "+str(amountdup)+" + "+str(extraamount)+" #DeFi on your way! #DeadFish #Ardor")
                        print(str(amount)+' You were not kind Zarks sent to: {}'.format(tweet['user']['screen_name']))
                    print(cnt)
    
            # Stops streaming when it reaches the limit
            if self.num_tweets <= TWEETS_TO_CAPTURE:
                if self.num_tweets % 100 == 0: # just to see some progress...
                    print('Numer of tweets captured so far: {}'.format(self.num_tweets))
                    return True
                else:
                    return False
                self.file.close()

    def on_error(self, status):
        print(status)


# Initialize Stream listener
l = MyStreamListener()

# Create you Stream object with authentication
stream = tweepy.Stream(auth, l)

# Filter Twitter Streams to capture data by the keywords:
while True:
    try:
        stream.filter(track=TRACKING_KEYWORDS, stall_warnings=True)
    except Exception as e:
        pass
