export interface Apartment {
    external_id: string;
    title: string;
    rooms: number;
    area_m2: number;
    floor: string | null;
    description: string;
    price: {
      value: number;
      currency: string;
    };
    location: {
      district: string;
      street: string;
      nearby: string | null;
    };
    building: {
      complex: string | null;
    };
    photo: {
      src: string;
    };
  }

