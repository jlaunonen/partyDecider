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
  HTTPValidationError,
  Message,
  NewVotingSession,
  VotingSession,
} from '../models';
import {
    AppFromJSON,
    AppToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    MessageFromJSON,
    MessageToJSON,
    NewVotingSessionFromJSON,
    NewVotingSessionToJSON,
    VotingSessionFromJSON,
    VotingSessionToJSON,
} from '../models';

export interface AddVotingSessionRequest {
    newVotingSession: NewVotingSession;
}

export interface CloseSessionRequest {
    voteSessionKey: string;
}

export interface SetEnabledRequest {
    requestBody: Array<number>;
    bySteamId?: boolean;
}

/**
 * 
 */
export class AdminApi extends runtime.BaseAPI {
    makeQueryParameters(queryParameters: any): string {
        if (Object.keys(queryParameters).length !== 0) {
            // only add the querystring to the URL if there are query parameters.
            // this is done to avoid urls ending with a "?" character which buggy webservers
            // do not handle correctly sometimes.
            return '?' + this.configuration.queryParamsStringify(queryParameters);
        }
        return "";
    }

    addVotingSession_Path(requestParameters: AddVotingSessionRequest): string {
        if (requestParameters.newVotingSession === null || requestParameters.newVotingSession === undefined) {
            throw new runtime.RequiredError('newVotingSession','Required parameter requestParameters.newVotingSession was null or undefined when calling addVotingSession.');
        }

        const queryParameters: any = {};


        const path = `/api/admin/voting`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Add Voting Session
     */
    async addVotingSessionRaw(requestParameters: AddVotingSessionRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VotingSession>> {
        if (requestParameters.newVotingSession === null || requestParameters.newVotingSession === undefined) {
            throw new runtime.RequiredError('newVotingSession','Required parameter requestParameters.newVotingSession was null or undefined when calling addVotingSession.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/admin/voting`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: NewVotingSessionToJSON(requestParameters.newVotingSession),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VotingSessionFromJSON(jsonValue));
    }

    /**
     * Add Voting Session
     */
    async addVotingSession(requestParameters: AddVotingSessionRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VotingSession> {
        const response = await this.addVotingSessionRaw(requestParameters, initOverrides);
        return await response.value();
    }

    closeSession_Path(requestParameters: CloseSessionRequest): string {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling closeSession.');
        }

        const queryParameters: any = {};


        const path = `/api/admin/voting/{vote_session_key}/close`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey)));

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Close Session
     */
    async closeSessionRaw(requestParameters: CloseSessionRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VotingSession>> {
        if (requestParameters.voteSessionKey === null || requestParameters.voteSessionKey === undefined) {
            throw new runtime.RequiredError('voteSessionKey','Required parameter requestParameters.voteSessionKey was null or undefined when calling closeSession.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/admin/voting/{vote_session_key}/close`.replace(`{${"vote_session_key"}}`, encodeURIComponent(String(requestParameters.voteSessionKey))),
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VotingSessionFromJSON(jsonValue));
    }

    /**
     * Close Session
     */
    async closeSession(requestParameters: CloseSessionRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VotingSession> {
        const response = await this.closeSessionRaw(requestParameters, initOverrides);
        return await response.value();
    }

    getAll_Path(): string {
        const queryParameters: any = {};


        const path = `/api/admin/all`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get all apps/games
     */
    async getAllRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<App>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/admin/all`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(AppFromJSON));
    }

    /**
     * Get all apps/games
     */
    async getAll(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<App>> {
        const response = await this.getAllRaw(initOverrides);
        return await response.value();
    }

    getEnabled_Path(): string {
        const queryParameters: any = {};


        const path = `/api/admin/enabled`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Get enabled apps/games
     */
    async getEnabledRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<App>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/admin/enabled`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(AppFromJSON));
    }

    /**
     * Get enabled apps/games
     */
    async getEnabled(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<App>> {
        const response = await this.getEnabledRaw(initOverrides);
        return await response.value();
    }

    rescanGames_Path(): string {
        const queryParameters: any = {};


        const path = `/api/admin/rescan`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Rescan all installed apps/games
     */
    async rescanGamesRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<number>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/admin/rescan`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        if (this.isJsonMime(response.headers.get('content-type'))) {
            return new runtime.JSONApiResponse<number>(response);
        } else {
            return new runtime.TextApiResponse(response) as any;
        }
    }

    /**
     * Rescan all installed apps/games
     */
    async rescanGames(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<number> {
        const response = await this.rescanGamesRaw(initOverrides);
        return await response.value();
    }

    setEnabled_Path(requestParameters: SetEnabledRequest): string {
        if (requestParameters.requestBody === null || requestParameters.requestBody === undefined) {
            throw new runtime.RequiredError('requestBody','Required parameter requestParameters.requestBody was null or undefined when calling setEnabled.');
        }

        const queryParameters: any = {};

        if (requestParameters.bySteamId !== undefined) {
            queryParameters['by_steam_id'] = requestParameters.bySteamId;
        }


        const path = `/api/admin/enabled`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * List of ID\'s (or Steam-ID\'s if by_steam_id is true) that should be enabled for voting.
     * Set enabled apps/games
     */
    async setEnabledRaw(requestParameters: SetEnabledRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Message>> {
        if (requestParameters.requestBody === null || requestParameters.requestBody === undefined) {
            throw new runtime.RequiredError('requestBody','Required parameter requestParameters.requestBody was null or undefined when calling setEnabled.');
        }

        const queryParameters: any = {};

        if (requestParameters.bySteamId !== undefined) {
            queryParameters['by_steam_id'] = requestParameters.bySteamId;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/admin/enabled`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: requestParameters.requestBody,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MessageFromJSON(jsonValue));
    }

    /**
     * List of ID\'s (or Steam-ID\'s if by_steam_id is true) that should be enabled for voting.
     * Set enabled apps/games
     */
    async setEnabled(requestParameters: SetEnabledRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Message> {
        const response = await this.setEnabledRaw(requestParameters, initOverrides);
        return await response.value();
    }

    shutdown_Path(): string {
        const queryParameters: any = {};


        const path = `/api/admin/shutdown`;

        return this.configuration.basePath + path + this.makeQueryParameters(queryParameters);
    }

    /**
     * Shutdown the server application
     */
    async shutdownRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Message>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/admin/shutdown`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MessageFromJSON(jsonValue));
    }

    /**
     * Shutdown the server application
     */
    async shutdown(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Message> {
        const response = await this.shutdownRaw(initOverrides);
        return await response.value();
    }

}
