// /app/utils/csvParser.ts
import fs from 'fs';
import { parse } from 'csv-parse';

export async function parseCsv(filePath: string): Promise<string[]> {
  const records: string[] = [];
  const parser = fs.createReadStream(filePath).pipe(parse({ columns: false }));

  for await (const record of parser) {
    records.push(record[0]); // Assuming usernames are in the first column
  }

  return records;
}
