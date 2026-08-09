export interface City {
  id: number;
  uid?: string | null;
  official_code?: string | null;
  name: string;
  english_name: string | null;
  latitude: string | number | null;
  longitude: string | number | null;
  is_capital: boolean;
  population: number | null;
  postal_code: string | null;
  county?: string | null;
  county_code?: string | null;
  district?: string | null;
  district_code?: string | null;
}

export interface Province {
  id: number;
  uid?: string | null;
  official_code?: string | null;
  province: string;
  english_name: string | null;
  phone_code: string | null;
  cities_count: number;
  cities: City[];
}

declare const iranCities: Province[];
export default iranCities;
