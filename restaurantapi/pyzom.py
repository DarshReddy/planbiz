from pyzomato import Pyzomato


class Exjson:
    def extract_element_from_json(obj, path):
        '''
        Extracts an element from a nested dictionary or
        a list of nested dictionaries along a specified path.
        If the input is a dictionary, a list is returned.
        If the input is a list of dictionary, a list of lists is returned.
        obj - list or dict - input dictionary or list of dictionaries
        path - list - list of strings that form the path to the desired element
        '''
        def extract(obj, path, ind, arr):
            '''pecified path and returns a list.
                obj - dict - input dictionary
                path - list
                Extracts an element from a nested dictionary
                along a s - list of strings that form the JSON path
                ind - int - starting index
                arr - list - output list
            '''
            key = path[ind]
            if ind + 1 < len(path):
                if isinstance(obj, dict):
                    if key in obj.keys():
                        extract(obj.get(key), path, ind + 1, arr)
                    else:
                        arr.append(None)
                elif isinstance(obj, list):
                    if not obj:
                        arr.append(None)
                    else:
                        for item in obj:
                            extract(item, path, ind, arr)
                else:
                    arr.append(None)
            if ind + 1 == len(path):
                if isinstance(obj, list):
                    if not obj:
                        arr.append(None)
                    else:
                        for item in obj:
                            arr.append(item.get(key, None))
                elif isinstance(obj, dict):
                    arr.append(obj.get(key, None))
                else:
                    arr.append(None)
            return arr
        if isinstance(obj, dict):
            return extract(obj, path, 0, [])
        elif isinstance(obj, list):
            outer_arr = []
            for item in obj:
                outer_arr.append(extract(item, path, 0, []))
            return outer_arr

p = Pyzomato("4d23393190ba2ae6c5b5298145c70f07")

class GetRst:
    def getRestaurants(lat,lon, *args):
        response = p.getByGeocode(lat,lon)
        rid = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","id"])
        data = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","name"])
        cost = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","average_cost_for_two"])
        img = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","featured_image"])   
        loc = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","location","locality_verbose"])
        url = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","url"])
        cuisines = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","cuisines"])
        rating = Exjson.extract_element_from_json(response,
            ["nearby_restaurants","restaurant","user_rating","aggregate_rating"])
        rst_list = []

        for b in args:
            bgt = b

        for x in range(0,len(Exjson.extract_element_from_json(response,["nearby_restaurants","restaurant"]))):
            if args:
                if cost[x]/2 <= bgt:
                    jso = {}
                    jso["Url"]=url[x]
                    jso["Img_url"]=img[x]
                    jso["Locality"]=loc[x]
                    jso["Avg_cost"]=cost[x]/2
                    jso["Name"]=data[x]
                    jso["Cuisines"]=cuisines[x]
                    jso["resID"]=rid[x]
                    jso["Rating"]=rid[x]
                    rst_list.append(jso.copy())
            else:
                jso = {}
                jso["Url"]=url[x]
                jso["Img_url"]=img[x]
                jso["Locality"]=loc[x]
                jso["Avg_cost"]=cost[x]/2
                jso["Name"]=data[x]
                jso["Cuisines"]=cuisines[x]
                jso["resID"]=rid[x]
                jso["Rating"]=rid[x]
                rst_list.append(jso.copy())

        return rst_list

    def getLocation(lat,lon, *args):
        response = p.getByGeocode(lat,lon)
        location = Exjson.extract_element_from_json(response,
            ["location","title"])
        return location

    def getRsts(lat,lon,*args):
        cng = 0.025
        loca = [(lat,lon),(lat-cng,lon),(lat,lon-cng),(lat-cng,lon-cng),(lat+cng,lon+cng),
				(lat+cng,lon),(lat,lon+cng)]
        all_rsts=[]
        for lat,lon in loca:
            if args:
                for arg in args:
                    rsts = GetRst.getRestaurants(lat,lon,arg)
            else:
                rsts = GetRst.getRestaurants(lat,lon)
            all_rsts+=rsts
        all_rsts = [dict(t) for t in {tuple(d.items()) for d in all_rsts}]
        return all_rsts
