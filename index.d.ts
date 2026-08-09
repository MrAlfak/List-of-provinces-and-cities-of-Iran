export interface City {
  /** Legacy-compatible numeric ID. Prefer uid/official_code for source identity. */
  id: number;
  /** Stable source-backed identifier. */
  uid: string;
  /** Composite official source hierarchy code for the pinned snapshot. */
  official_code: string;
  name: string;
  /** Optional enrichment; may be null until reviewed. */
  english_name: string | null;
  /** Optional enrichment; may be null. */
  latitude: string | number | null;
  /** Optional enrichment; may be null. */
  longitude: string | number | null;
  is_capital: boolean;
  population: number | null;
  postal_code: string | null;
  county: string | null;
  county_code: string;
  district: string | null;
  district_code: string;
}

export interface Province {
  id: number;
  uid: string;
  official_code: string;
  province: string;
  english_name: string | null;
  phone_code: string | null;
  cities_count: number;
  /** Canonical source snapshot marker; current dataset uses 1402. */
  last_updated: string;
  cities: City[];
}

declare const iranCities: Province[];
export default iranCities;
