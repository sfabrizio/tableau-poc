import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface TableauView {
  view_id: string;
  view_name: string;
  content_url: string;
}

interface TableauWorkbook {
  workbook_id: string;
  workbook_name: string;
  views: TableauView[];
}

@Injectable({
  providedIn: 'root'
})
export class TableauService {
  private readonly apiBaseUrl = 'http://localhost:5000/api/tableau';

  constructor(private http: HttpClient) {}

  getEmbedUrl(workbookId: string, viewId: string): Observable<{embedUrl: string}> {
    return this.http.get<{embedUrl: string}>(`${this.apiBaseUrl}/embed?workbookId=${workbookId}&viewId=${viewId}`);
  }

  getWorkbooks(): Observable<TableauWorkbook[]> {
    return this.http.get<TableauWorkbook[]>(`${this.apiBaseUrl}/workbooks`);
  }
}
