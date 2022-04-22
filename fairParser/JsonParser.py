from FSON import DICT
from FDate import DATE
from fairParser import Keys

# Log = Log("FAIR.Parser.JsonParser")

keys = Keys.keys

def parse(data, parseAll=False) -> {}:
    print(f"Parsing data IN=[ {data} ]")
    try:
        json_obj = {}
        json_obj["author"] = DICT.get_all_keys(data, keys("author"), force_type=True)
        json_obj["title"] = DICT.get_all_keys(data, keys("title"), force_type=True)
        json_obj["description"] = DICT.get_all_keys(data, keys("description"), force_type=True)
        json_obj["body"] = DICT.get_all_keys(data, keys("body"), force_type=True)
        json_obj["url"] = DICT.get_all_keys(data, keys("url"), force_type=True)
        json_obj["img_url"] = DICT.get_all_keys(data, keys("imgUrl"), force_type=True)
        json_obj["source"] = DICT.get_all_keys(data, keys("source_url"), force_type=True)
        json_obj["tickers"] = DICT.get_all_keys(data, keys("tickers"))
        json_obj["tags"] = DICT.get_all_keys(data, keys("tags"))
        temp_date = DICT.get_all_keys(data, keys("published_date"))
        json_obj["published_date"] = DATE.parse_obj_to_month_day_year_str(temp_date)

        if parseAll:
            json_obj["summary"] = DICT.get("summary", data)
            json_obj["comments"] = DICT.get("comments", data)
            json_obj["source_rank"] = DICT.get("source_rank", data)
            json_obj["category"] = DICT.get("category", data)
            json_obj["sentiment"] = DICT.get("sentiment", data)
            json_obj["category_scores"] = DICT.get("category_scores", data)
            json_obj["score"] = DICT.get("score", data)
            json_obj["title_score"] = DICT.get("title_score", data)
            json_obj["description_score"] = DICT.get("description_score", data)
            json_obj["body_score"] = DICT.get("body_score", data)

        print(f"Parsing data OUT=[ {json_obj} ]")
        return json_obj
    except Exception as e:
        print(f"Failed to parse data=[ {data} ], error=[ {e} ]")
        return None