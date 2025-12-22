export interface Apartment {
    external_id: string;
    title: string;
    room_count: number;
    area: number;
    floor: string | null;
    description: string;
    price: number,
    location: {
      region_name: string;
      address: string;
    };
    complex: string | null;
    photo: string;
  }

