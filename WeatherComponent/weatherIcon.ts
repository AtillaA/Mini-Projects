/**
 * WeatherAPI condition code -> Material Icons
 * Full code list: https://www.weatherapi.com/docs/weather_conditions.json
 * Handled in weatherIcon()
 */
const ICON_GROUPS: [icon: string, codes: number[]][] = [
    ['cloud',        [1006, 1009]],
    ['foggy',        [1012, 1030, 1033, 1036, 1039, 1042, 1135, 1147]],
    ['air',          [1015, 1018, 1021, 1024, 1027, 1045, 1048]],
    ['water_drop',   [1063, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189,
                      1192, 1195, 1198, 1201, 1240, 1243, 1246]],
    ['grain',        [1069, 1204, 1207, 1237, 1249, 1252, 1261, 1264]],
    ['ac_unit',      [1066, 1114, 1117, 1210, 1213, 1216, 1219, 1222, 1225, 1255, 1258]],
    ['thunderstorm', [1087, 1273, 1276, 1279, 1282]]
];

const ICON_BY_CODE = new Map<number, string>(
    ICON_GROUPS.flatMap(([icon, codes]) => codes.map((code) => [code, icon] as [number, string]))
);

/** icon for a WeatherAPI condition - unknown codes fall back to a plain cloud */
export function weatherIcon(code: number, isDay: boolean): string {
    if (code === 1000) { return isDay ? 'wb_sunny' : 'dark_mode'; }
    if (code === 1003) { return isDay ? 'filter_drama' : 'nights_stay'; }
    
    return ICON_BY_CODE.get(code) ?? 'cloud';
}
