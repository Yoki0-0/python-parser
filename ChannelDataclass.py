from dataclasses import dataclass

@dataclass
class Channel:
    name: str
    link: str
    category: str
    subs: int
    avg_views_post: int
    err: float
    migr_sub7d: int
    migr_sub30d: int
    lifetime: str