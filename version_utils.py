import json
import urllib2
from directories import userCachePath
import os
import time
import urllib
from PIL import Image
from urllib2 import HTTPError
import atexit
import threading
import logging
from uuid import UUID

logger = logging.getLogger()

def deprecated(func):
    def new_func(*args, **kwargs):
        #logger.warn("Function \""+str(func.__name__)+"\" is deprecated and should not be used")
        return func(*args, **kwargs)   
    new_func.__name__ = func.__name__
    if func.__doc__ is not None:
        new_func.__doc__ = '''*Deprecated*\n%s'''%func.__doc__
    else:
        new_func.__doc__ = '''*Deprecated*'''
    new_func.__dict__.update(func.__dict__)
    return new_func


class PlayerCache:
    '''
    Used to cache Player names and UUID's, provides an small API to interface with it
    '''
    
    _playerCacheList = []

    def __convert(self):
        jsonFile = None
        fp = open(userCachePath)
        try:
            jsonFile = json.load(fp)
            fp.close()
        except ValueError:
            fp.close()
            # Assuming JSON file is corrupted, deletes file and creates new one
            os.remove(userCachePath)
            with open(userCachePath, 'w') as json_out:
                json.dump([], json_out)
        if jsonFile is not None:
            for old_player in jsonFile.keys():
                player = jsonFile[old_player]
                new_player = {"Playername": player["username"], "UUID (No Separator)": old_player.replace("-", ""),
                              "UUID (Separator)": old_player, "WasSuccessful": True, "Timstamp": player["timestamp"]}
                self._playerCacheList.append(new_player)
            self._save()
            print "Convert usercache.json"
            
    def fixAllOfPodshotsBugs(self):
        '''
        Convenient function that fixes any bugs/typos (in the usercache.json file) that Podshot may have created
        '''
        for player in self._playerCacheList:
            if "Timstamp" in player:
                player["Timestamp"] = player["Timstamp"]
                del player["Timstamp"]
        self._save()
    
    def load(self):
        '''
        Loads from the usercache.json file if it exists, if not an empty one will be generated
        '''
        if not os.path.exists(userCachePath):
            out = open(userCachePath, 'w') 
            json.dump(self._playerCacheList, out)
            out.close()
        f = open(userCachePath, 'r')
        line = f.readline()
        if line.startswith("{"):
            f.close()
            self.__convert()
        f.close()
        try:
            json_in = open(userCachePath)
            self._playerCacheList = json.load(json_in)
        except:
            logger.warning("Usercache.json may be corrupted")
            self._playerCacheList = []
        finally:
            json_in.close()
        self.fixAllOfPodshotsBugs()
        self.refresh_lock = threading.Lock()
        self.player_refreshing = threading.Thread(target=self._refreshAll)
        self.player_refreshing.daemon = True
        self.player_refreshing.start()     

    def _save(self):
        out = open(userCachePath, "w")
        json.dump(self._playerCacheList, out, indent=4, separators=(',', ':'))
        out.close()
            
    def _removePlayerWithName(self, name):
        toRemove = None
        for p in self._playerCacheList:
            if p["Playername"] == name:
                toRemove = p
        if toRemove is not None:
            self._playerCacheList.remove(toRemove)
            self._save()
    
    def _removePlayerWithUUID(self, uuid, seperator=True):
        toRemove = None
        for p in self._playerCacheList:
            if seperator:
                if p["UUID (Separator)"] == uuid:
                    toRemove = p
            else:
                if p["UUID (No Separator)"] == uuid:
                    toRemove = p
        if toRemove is not None:
            self._playerCacheList.remove(toRemove)
            self._save()
            
    def nameInCache(self, name):
        '''
        Checks to see if the name is already in the cache
        
        :param name: The name of the player
        :type name: str
        :rtype: bool
        '''
        isInCache = False
        for p in self._playerCacheList:
            if p["Playername"] == name:
                isInCache = True
        return isInCache
    
    def uuidInCache(self, uuid, seperator=True):
        '''
        Checks to see if the UUID is already in the cache
        
        :param uuid: The UUID of the player
        :type uuid: str
        :param seperator: True if the UUID has separators ('-')
        :type seperator: bool
        :rtype: bool
        '''
        isInCache = False
        for p in self._playerCacheList:
            if seperator:
                if p["UUID (Separator)"] == uuid:
                    isInCache = True
            else:
                if p["UUID (No Separator)"] == uuid:
                    isInCache = True
        return isInCache
    
    def _refreshAll(self):
        with self.refresh_lock:
            playersNeededToBeRefreshed = []
            try:
                t = time.time()
            except:
                t = 0
            for player in self._playerCacheList:
                if player["Timestamp"] != "<Invalid>":
                    if t - player["Timestamp"] > 21600:
                        playersNeededToBeRefreshed.append(player)
            for player in playersNeededToBeRefreshed:
                self.getPlayerFromUUID(player["UUID (Separator)"], forceNetwork=True, dontSave=True)
                self._save()
    
    def force_refresh(self):
        '''
        Refreshes all players in the cache, regardless of how long ago the name was synced
        '''
        players = self._playerCacheList
        for player in players:
            self.getPlayerInfo(player["UUID (Separator)"], force=True)
            
    @deprecated
    def getPlayerFromUUID(self, uuid, forceNetwork=False, dontSave=False):
        player = {}
        response = None
        if forceNetwork:
            if self.uuidInCache(uuid):
                self._removePlayerWithUUID(uuid)
            try:
                response = urllib2.urlopen("https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid.replace("-",""))).read()
            except urllib2.URLError:
                return uuid
            if response is not None and response != "":
                playerJSON = json.loads(response)
                player["Playername"] = playerJSON["name"]
                player["UUID (No Separator)"] = playerJSON["id"]
                player["UUID (Separator)"] = uuid
                player["WasSuccessful"] = True
                player["Timestamp"] = time.time()
                self._playerCacheList.append(player)
                if not dontSave:
                    self._save()
                return playerJSON["name"]
            else:
                return uuid
        else:
            couldNotFind = False
            for p in self._playerCacheList:
                if p["UUID (Separator)"] == uuid and p["WasSuccessful"]:
                    couldNotFind = False
                    return p["Playername"]
                else:
                    couldNotFind = True
            if couldNotFind:
                result = self.getPlayerFromUUID(uuid, forceNetwork=True)
                if result == uuid:
                    player = {"Playername":"<Unknown>","UUID (Separator)":uuid,"UUID (No Separator)":uuid.replace("-",""),"Timestamp":"<Invalid>","WasSuccessful":False}
                    self._playerCacheList.append(player)
                    return uuid
    @deprecated
    def getPlayerFromPlayername(self, playername, forceNetwork=False, separator=True):
        response = None
        if forceNetwork:
            if self.nameInCache(playername):
                self._removePlayerWithName(playername)
            try:
                response = urllib2.urlopen("https://api.mojang.com/users/profiles/minecraft/{}".format(playername)).read()
            except urllib2.URLError:
                return playername
            if response is not None and response != "":
                playerJSON = json.loads(response)
                player = {"Playername": playername, "UUID (No Separator)": playerJSON["id"]}
                uuid = playerJSON["id"][:8]+"-"+playerJSON["id"][8:12]+"-"+playerJSON["id"][12:16]+"-"+playerJSON["id"][16:20]+"-"+playerJSON["id"][20:]
                player["UUID (Separator)"] = uuid
                player["WasSuccessful"] = True
                player["Timestamp"] = time.time()
                self._playerCacheList.append(player)
                self._save()
                if separator:
                    return uuid
                else:
                    return playerJSON["id"]
            else:
                return playername
        else:
            couldNotFind = False
            for p in self._playerCacheList:
                if p["Playername"] == playername and p["WasSuccessful"]:
                    couldNotFind = False
                    return p["UUID (Separator)"]
                else:
                    couldNotFind = True
            if couldNotFind:
                result = self.getPlayerFromPlayername(playername, forceNetwork=True)
                if result == playername:
                    player = {"Playername":playername,"UUID (Separator)":"<Unknown>","UUID (No Separator)":"<Unknown>","Timestamp":"<Invalid>","WasSuccessful":False}
                    self._playerCacheList.append(player)
                    return playername
    
    # 0 if for a list of the playernames, 1 is for a dictionary of all player data
    def getAllPlayersKnown(self, returnType=0, include_failed_lookups=False):
        '''
        Returns all players in the cache
        
        :param returnType: What type should be returned, 0 for a list of playernames, 1 for a dictionary of player data, with the key being the player name
        :type returnType: int
        :param include_failed_lookups: Whether all current failed lookups also be included
        :type include_failed_lookups: bool
        :return: All player data in the specified data structure
        :rtype: list or dict
        '''
        toReturn = None
        if returnType == 0:
            toReturn = []
            for p in self._playerCacheList:
                if p["WasSuccessful"]:
                    toReturn.append(p["Playername"])
                elif include_failed_lookups:
                    toReturn.append(p["Playername"])      
        elif returnType == 1:
            toReturn = {}
            for p in self._playerCacheList:
                if p["WasSuccessful"]:
                    toReturn[p["Playername"]] = p
                elif include_failed_lookups:
                    toReturn[p["Playername"]] = p
        return toReturn
    
    def getFromCacheUUID(self, uuid, seperator=True):
        '''
        Checks if the UUID is already in the cache
        
        :param uuid: The UUID that might be in the cache
        :type uuid: str
        :param seperator: Whether the UUID is seperated by -'s
        :type seperator: bool
        :return: The player data that is in the cache for the specified UUID, same format as getPlayerInfo()
        :rtype: tuple
        '''
        for player in self._playerCacheList:
            if seperator and player["UUID (Separator)"] == uuid:
                return player["UUID (Separator)"], player["Playername"], player["UUID (No Separator)"]
            elif player["UUID (No Separator)"] == uuid:
                return player["UUID (Separator)"], player["Playername"], player["UUID (No Separator)"]
            
    def getFromCacheName(self, name):
        '''
        Checks if the Player name is already in the cache
        
        :param name: The name of the Player that might be in the cache
        :return: The player data that is in the cache for the specified Player name, same format as getPlayerInfo()
        :rtype: tuple
        '''
        for player in self._playerCacheList:
            if name == player["Playername"]:
                return player["UUID (Separator)"], player["Playername"], player["UUID (No Separator)"]
    
    def getPlayerInfo(self, arg, force=False):
        '''
        Recommended method to call to get Player data. Roughly determines whether a UUID or Player name was passed in 'arg'
        
        :param arg: Either a UUID or Player name to retrieve from the cache/Mojang
        :type arg: str
        :param force: True if the Player name should be forcefully fetched from Mojang
        :type force: bool
        :return: A tuple with the data in this order: (UUID with separator, Player name, UUID without separator)
        :rtype: tuple
        '''
        try:
            UUID(arg, version=4)
            if self.uuidInCache(arg) and not force:
                return self.getFromCacheUUID(arg)
            else:
                return self._getPlayerInfoUUID(arg)
        except ValueError:
            if self.nameInCache(arg) and not force:
                return self.getFromCacheName(arg)
            else:
                return self._getPlayerInfoName(arg)
        
    def _getPlayerInfoUUID(self, uuid):
        response_name = None
        response_uuid = None
        player = {}
        if self.uuidInCache(uuid):
            self._removePlayerWithUUID(uuid)
        try:
            response_uuid = json.loads(urllib2.urlopen("https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid.replace("-", ""))).read())
            response_name = json.loads(urllib2.urlopen("https://api.mojang.com/users/profiles/minecraft/{}".format(response_uuid["name"])).read())
        except urllib2.URLError:
            return uuid
        except ValueError:
            print "Caught value error while getting player info for "+uuid
            return uuid
        if response_name is not None and response_name != "" and response_uuid is not None and response_uuid != "":
            player["Playername"] = response_name["name"]
            player["UUID (Separator)"] = response_name["id"][:8]+"-"+response_name["id"][8:12]+"-"+response_name["id"][12:16]+"-"+response_name["id"][16:20]+"-"+response_name["id"][20:]
            player["UUID (No Separator)"] = response_name["id"]
            player["WasSuccessful"] = True
            player["Timestamp"] = time.time()
            self._playerCacheList.append(player)
            self._save()
            return player["UUID (Separator)"], player["Playername"], player["UUID (No Separator)"]
        else:
            return uuid
            #raise Exception("Couldn't find player")
    
    def _getPlayerInfoName(self, playername):
        response_name = None
        response_uuid = None
        player = {}
        if self.nameInCache(playername):
            self._removePlayerWithName(playername)
        try:
            response_name = json.loads(urllib2.urlopen("https://api.mojang.com/users/profiles/minecraft/{}".format(playername)).read())
            response_uuid = json.loads(urllib2.urlopen("https://sessionserver.mojang.com/session/minecraft/profile/{}".format(response_name["id"])).read())
        except urllib2.URLError:
            return playername
        except ValueError:
            print "Caught value error while getting player info for "+playername
            return playername
        if response_name is not None and response_name != "" and response_uuid is not None and response_uuid != "":
            player["Playername"] = response_name["name"]
            player["UUID (Separator)"] = response_name["id"][:8]+"-"+response_name["id"][8:12]+"-"+response_name["id"][12:16]+"-"+response_name["id"][16:20]+"-"+response_name["id"][20:]
            player["UUID (No Separator)"] = response_name["id"]
            player["WasSuccessful"] = True
            player["Timestamp"] = time.time()
            self._playerCacheList.append(player)
            self._save()
            return player["UUID (Separator)"], player["Playername"], player["UUID (No Separator)"]
        else:
            return playername
            #raise Exception("Couldn't find player")
    
    @staticmethod
    def __formats():
        player = {
                  "Playername":"<Username>",
                  "UUID":"<uuid>",
                  "Timestamp":"<timestamp>",
                  # WasSuccessful will be true if the UUID/Player name was retrieved successfully
                  "WasSuccessful":True
                  }
        pass
    
    def cleanup(self):
        '''
        Removes all failed UUID/Player name lookups from the cache
        '''
        remove = []
        for player in self._playerCacheList:
            if not player["WasSuccessful"]:
                remove.append(player)
        for toRemove in remove:
            self._playerCacheList.remove(toRemove)
        self._save()
         
_playercache = PlayerCache()
_playercache.load()
playercache = _playercache
            
@deprecated
def getUUIDFromPlayerName(player, seperator=True, forceNetwork=False):
    '''
    Old compatibility function for the PlayerCache method. It is recommended to use playercache.getPlayerInfo()
    '''
    return playercache.getPlayerFromPlayername(player, forceNetwork, seperator)

@deprecated
def getPlayerNameFromUUID(uuid,forceNetwork=False):
    '''
    Old compatibility function for the PlayerCache method. It is recommended to use playercache.getPlayerInfo()
    '''
    return playercache.getPlayerFromUUID(uuid, forceNetwork)     

def getPlayerSkin(uuid, force=False, trying_again=False, instance=None):
    '''
    Gets the player's skin from Mojang's skin servers
    
    :param uuid: The UUID of the player
    :type uuid: str
    :param force: Should the skin be redownloaded even if it has already been downloaded
    :type force: bool
    :param trying_again: True if the method already failed once
    :type trying_again: bool
    :param instance: The instance of the PlayerTool
    :type instance: PlayerTool
    :return: The path to the player skin
    :rtype: str
    '''
    SKIN_URL = "http://skins.minecraft.net/MinecraftSkins/{}.png"
    toReturn = 'char.png'
    try:
        os.mkdir("player-skins")
    except OSError:
        pass
    if force or not os.path.exists(os.path.join("player-skins", uuid.replace("-", "_")+".png")):
        try:
            # Checks to see if the skin even exists
            urllib2.urlopen(SKIN_URL.format(playercache.getPlayerFromUUID(uuid, forceNetwork=False)))
        except urllib2.URLError as e:
            if "Not Found" in e.msg:
                return toReturn
    try:
        if os.path.exists(os.path.join("player-skins", uuid.replace("-", "_")+".png")) and not force:
            player_skin = Image.open(os.path.join("player-skins", uuid.replace("-","_")+".png"))
            if player_skin.size == (64,64):
                player_skin = player_skin.crop((0,0,64,32))
                player_skin.save(os.path.join("player-skins", uuid.replace("-","_")+".png"))
            toReturn = os.path.join("player-skins", uuid.replace("-","_")+".png")
        else:
            playername = playercache.getPlayerFromUUID(uuid,forceNetwork=False)
            urllib.urlretrieve(SKIN_URL.format(playername), os.path.join("player-skins", uuid.replace("-","_")+".png"))
            toReturn = os.path.join("player-skins", uuid.replace("-","_")+".png")
            player_skin = Image.open(toReturn)
            if player_skin.size == (64,64):
                player_skin = player_skin.crop((0,0,64,32))
                player_skin.save(os.path.join("player-skins", uuid.replace("-","_")+".png"))
    except IOError:
        print "Couldn't find Image file ("+str(uuid.replace("-","_")+".png")+") or the file may be corrupted"
        print "Trying to re-download skin...."
        if not trying_again and instance is not None:
            instance.delete_skin(uuid)
            os.remove(os.path.join("player-skins", uuid.replace("-","_")+".png"))
            toReturn = getPlayerSkin(uuid, force=True, trying_again=True)
        pass
    except HTTPError:
        print "Couldn't connect to a network"
        raise Exception("Could not connect to the skins server, please check your Internet connection and try again.")
        pass
    except Exception:
        print "Unknown error occurred while reading/downloading skin for "+str(uuid.replace("-","_")+".png")
        pass
    return toReturn

def _cleanup():
    if os.path.exists("player-skins"):
        for image_file in os.listdir("player-skins"):
            fp = None
            try:
                fp = open(os.path.join("player-skins", image_file), 'rb')
                Image.open(fp)
            except IOError:
                fp.close()
                os.remove(os.path.join("player-skins", image_file))
    playercache.cleanup()
    
atexit.register(_cleanup)

