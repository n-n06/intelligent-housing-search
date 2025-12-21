from enum import Enum

class AlmatyRegion(str, Enum):
    alatau = "alatau"
    almaly = "almaly"
    auezov = "auezov"
    bostandyk = "bostandyk"
    medeu = "medeu"
    nauryzbay = "nauryzbay"
    turksib = "turksib"
    zhetysu = "zhetysu"

    @property
    def path(self) -> str:
        return {
            AlmatyRegion.alatau: "alatauskij",
            AlmatyRegion.almaly: "almalinskij",
            AlmatyRegion.auezov: "aujezovskij",
            AlmatyRegion.bostandyk: "bostandykskij",
            AlmatyRegion.medeu: "medeuskij",
            AlmatyRegion.nauryzbay: "nauryzbajskiy",
            AlmatyRegion.turksib: "turksibskij",
            AlmatyRegion.zhetysu: "zhetysuskij",
        }[self]

    @property
    def display_name(self) -> str:
        return {
            AlmatyRegion.alatau: "Алатауский р-н",
            AlmatyRegion.almaly: "Алмалинский р-н",
            AlmatyRegion.auezov: "Ауэзовский р-н",
            AlmatyRegion.bostandyk: "Бостандыкский р-н",
            AlmatyRegion.medeu: "Медеуский р-н",
            AlmatyRegion.nauryzbay: "Наурызбайский р-н",
            AlmatyRegion.turksib: "Турксибский р-н",
            AlmatyRegion.zhetysu: "Жетысуский р-н",
        }[self]


class ListingType(str, Enum):
    rent = "rent"
    sell = "sell"

    @property
    def path(self) -> str:
        return {
            ListingType.rent: "arenda",
            ListingType.sell: "prodazha"
        }[self]

    @property
    def display_name(self) -> str:
        return {
            ListingType.rent: "Аренда",
            ListingType.sell: "Продажа"
        }[self]

class ListingTypeDisplay(str, Enum):
    rent = "Аренда"
    sell = "Продажа"
