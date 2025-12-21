export interface Apartment {
    external_id: string;
    title: string;
    room_count: number;
    area: number;
    floor: string | null;
    description: string;
    price: number,
    location: {
      region: string;
      street: string;
    };
    complex: string | null;
    photo: string;
  }

