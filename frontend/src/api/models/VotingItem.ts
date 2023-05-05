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

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface VotingItem
 */
export interface VotingItem {
    /**
     * 
     * @type {number}
     * @memberof VotingItem
     */
    id: number;
    /**
     * 
     * @type {number}
     * @memberof VotingItem
     */
    steamId: number;
    /**
     * 
     * @type {string}
     * @memberof VotingItem
     */
    name: string;
    /**
     * 
     * @type {number}
     * @memberof VotingItem
     */
    score?: number;
}

/**
 * Check if a given object implements the VotingItem interface.
 */
export function instanceOfVotingItem(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "steamId" in value;
    isInstance = isInstance && "name" in value;

    return isInstance;
}

export function VotingItemFromJSON(json: any): VotingItem {
    return VotingItemFromJSONTyped(json, false);
}

export function VotingItemFromJSONTyped(json: any, ignoreDiscriminator: boolean): VotingItem {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'steamId': json['steam_id'],
        'name': json['name'],
        'score': !exists(json, 'score') ? undefined : json['score'],
    };
}

export function VotingItemToJSON(value?: VotingItem | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'steam_id': value.steamId,
        'name': value.name,
        'score': value.score,
    };
}

