// TypeScript definitions for iran-cities-data

export interface City {
  id: number;
  name: string;
  english_name: string;
  latitude: string;
  longitude: string;
  is_capital: boolean;
  population: number | null;
  postal_code: string | null;
}

export interface Province {
  id: number;
  province: string;
  english_name: string;
  phone_code: string;
  cities_count: number;
  cities: City[];
}

declare const iranCities: Province[];
export default iranCities;
