import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TableauService {
  private readonly apiBaseUrl = '/api/tableau';

  constructor(private http: HttpClient) {}

  getEmbedUrl(workbookId: string, viewId: string): Observable<string> {
    return this.http.get<string>(`${this.apiBaseUrl}/embed?workbookId=${workbookId}&viewId=${viewId}`);
  }
}
