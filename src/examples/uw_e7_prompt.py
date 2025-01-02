import cohere


def query_cohere(client: cohere.ClientV2, prompt: str) -> str:
    return (
        client.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt}],
        )
        .message.content[0]
        .text
    )


waypoints_config = {
    "E7 Coffee and Donuts": {
        "x": 1,
        "y": 10,
        "floor": 1,
        "keywords": ["coffee", "food and drink", "snacks"],
        "aliases": ["E7 Cafe", "CnD"],
    },
    "1st floor Elevators": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["elevator"],
    },
    "E7 North Entrance": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["entrance"],
    },
    "E7 East Entrance": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["entrance"],
    },
    "E7 South Entrance": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["entrance"],
    },
    "Outreach Classroom": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["classroom", "lecture hall"],
    },
    "RoboHub Door": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["robots", "workshop"],
    },
    "RoboHub": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["robots", "workshop"],
    },
    "Vending Machine": {
        "x": 1,
        "y": 1,
        "floor": 1,
        "keywords": ["food and drink", "snacks"],
    },
    "Room 2106": {
        "x": 1,
        "y": 1,
        "floor": 2,
        "keywords": ["office", "zach", "WEEF"],
    },
}

prompt = """
You control a robot that can navigate through a building based on a json instruction format,
you understand several waypoints that have been given to you before (you can use RAG to retrieve
what room numbers or waypoints correspond to which people or semantics).

Here are all the waypoints you have access to:
{{ waypoints_list }}

Here are all the functions you have access to:
{"navigate": {waypoint [json]}}
{"wait": seconds [int]}
{"speak": speech [string]}

Remember that in the example prompts below, anytime you see _, you should replace it with the
appropriate information based on the previously provided waypoints list.

Example Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

Example Answer:
{
    "actions": [
        {
            "navigate": {
                "name": "Room 2106",
                "x": _,
                "y": _,
                "floor": _,
                "keywords": ["office", "zach", "WEEF"]
            }
        },
        {
            "navigate": {
                "name": "RoboHub Entrance",
                "x": _,
                "y": _,
                "floor": _
                "keywords": ["workshop", "robots"]
            }
        }
    ]
}

Example Prompt: Can you ask Zach for a key and drop it off at the RoboHub? Wait for 10 seconds for Zach to give you the key.

Example Answer:
{
    "actions": [
        {
            "navigate": {
                "name": "Room 2106",
                "x": _,
                "y": _,
                "floor": _,
                "keywords": ["office", "zach", "WEEF"],
            }
        },
        {
            "speak": "Can I have the key?"
        },
        {
            "wait": 10
        },
        {
            "navigate": {
                "name": "RoboHub Entrance",
                "x": _,
                "y": _,
                "floor": _,
                "keywords": ["workshop", "robots"],
            }
        }
    ]
}

Prompt: 
"""
