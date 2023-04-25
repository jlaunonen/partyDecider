/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  App,
} from '../models';
import {
    AppFromJSON,
    AppToJSON,
} from '../models';

/**
 * 
 */
export class PublicApi extends runtime.BaseAPI {
    makeQueryParameters(queryParameters: any): string {
        if (Object.keys(queryParameters).length !== 0) {
            // only add the querystring to the URL if there are query parameters.
            // this is done to avoid urls ending with a "?" character which buggy webservers
            // do not handle correctly sometimes.
            return '?' + this.configuration.queryParamsStringify(queryParameters);
        }
        return "";
    }

    getApps_Path(): string {
        const queryParameters: any = {};


        const path = `/api/apps`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get enabled apps/games.
     */
    async getAppsRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<App>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/apps`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(AppFromJSON));
    }

    /**
     * Get enabled apps/games.
     */
    async getApps(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<App>> {
        const response = await this.getAppsRaw(initOverrides);
        return await response.value();
    }

    getVotings_Path(): string {
        const queryParameters: any = {};


        const path = `/api/votings`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get currently active voting sessions.
     */
    async getVotingsRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/votings`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Get currently active voting sessions.
     */
    async getVotings(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.getVotingsRaw(initOverrides);
        return await response.value();
    }

    submitBallot_Path(): string {
        const queryParameters: any = {};


        const path = `/api/votings`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Submit ballot for voting session.
     */
    async submitBallotRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/votings`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<any>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Submit ballot for voting session.
     */
    async submitBallot(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.submitBallotRaw(initOverrides);
        return await response.value();
    }

}
